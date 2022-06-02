from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.http import HttpResponse

from plotly.io import from_json

from pyslope.pyslope import utilities
from plotly import graph_objects as go

# import backend section of code
import os
import sys

from pyslope.pyslope import (
    Slope,
    Material,
    Udl,
    LineLoad,
    COLOUR_FOS_DICT,
)

from .models import (
    MaterialModel,
    UdlModel,
    LineLoadModel,
)

from .forms import (
    SlopeForm,
    MaterialForm,
    UdlForm,
    LineLoadForm,
    AnalysisOptionsForm,
    WaterTableForm,
    LimitsForm,
)

sys.path.insert(0, os.path.abspath("../../"))

MAX_COLOUR_KEY = max(COLOUR_FOS_DICT)


def reset(request):
    # remove all saved information to allow the form to reset to default parameters
    request.session["forms"] = []
    request.session["plot_json"] = []
    request.session["search"] = []
    # get request the main page, however now session information is set to none meaning
    # that the default values are returned to the user.
    return redirect("index")


def pdf(request, max_fos=5):
    # get saved data, still taking forever.
    if request.session["plot_json"] == [] or request.session["search"] == []:
        return redirect("index")
    plot = from_json(request.session["plot_json"])
    search = list(eval(str(request.session["search"])))

    max_fos = float(max_fos)

    # turn json data back into a plotly chart
    traces = []

    for i in search:

        FOS = i["FOS"]
        if FOS < max_fos:

            c_x = i["c_x"]
            c_y = i["c_y"]
            radius = i["radius"]
            l_c = i["l_c"]
            r_c = i["r_c"]

            color = COLOUR_FOS_DICT[min(round(FOS, 1), MAX_COLOUR_KEY)]

            # generate points for circle, generates points only along bottom half of circle
            x, y = utilities.generate_circle_coordinates(c_x, c_y, radius)

            # empty vectors for circle points that we will actually include
            x_ = []
            y_ = []

            # 65 long list but the last half of points are for the top half of
            # circle and so will never actually be required.
            for i in range(len(x)):
                # x coordinate should be between left and right
                # note for y, should be less than left y but can stoop
                # below right i
                if x[i] <= r_c[0] and x[i] >= l_c[0] and y[i] <= l_c[1]:
                    x_.append(x[i])
                    y_.append(y[i])

            x_ = [l_c[0]] + x_ + [r_c[0]]
            y_ = [l_c[1]] + y_ + [r_c[1]]

            traces.append(
                {
                    "hovertemplate": "%{meta[0]}",
                    "line": {"color": color},
                    "meta": [round(FOS, 3)],
                    "mode": "lines",
                    "name": "",
                    "x": x_,
                    "y": y_,
                    "type": "scatter",
                }
            )

    traces.reverse()

    temp = plot.to_dict()
    temp["data"] = tuple(list(temp["data"]) + traces)

    plot = go.Figure(temp)

    # return pdf and redirect?
    pdf = plot.to_image(format="pdf", width=1600, height=900)

    response = HttpResponse(pdf, content_type="application/pdf")
    filename = "report.pdf"
    content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content

    return response


def index(request):

    # create formsets
    MaterialFormSet = modelformset_factory(MaterialModel, MaterialForm, extra=1)
    UdlFormSet = modelformset_factory(UdlModel, UdlForm, extra=1)
    LineLoadFormSet = modelformset_factory(LineLoadModel, LineLoadForm, extra=1)

    if request.method == "GET":
        # if forms have been saved initialise with previous data, otherwise reset.
        # if clear form button has been called then also dont use previous and use default.
        if (
            request.session.get("forms")
            and request.session.get("search")
            and request.session.get("plot_json")
        ):
            previous_forms = request.session.get("forms")
            search = request.session.get("search")
            plot_json = request.session.get("plot_json")
            # try load up the previous form information
            # if there is an error it is probably due to a version change.
            # clearing the beam will help rectify the issue.
            try:
                slope_form = SlopeForm(previous_forms, prefix="slope")

                material_formset = MaterialFormSet(previous_forms, prefix="material")
                udl_formset = UdlFormSet(previous_forms, prefix="udl")
                line_load_formset = LineLoadFormSet(previous_forms, prefix="lineload")

                water_table_form = WaterTableForm(previous_forms, prefix="watertable")
                limits_form = LimitsForm(previous_forms, prefix="limits")
                options_form = AnalysisOptionsForm(previous_forms, prefix="options")

            except Exception:
                return redirect("reset")

        else:
            slope_form = SlopeForm(prefix="slope")

            material_formset = MaterialFormSet(
                queryset=MaterialModel.objects.none(), prefix="material"
            )
            udl_formset = UdlFormSet(queryset=UdlModel.objects.none(), prefix="udl")
            line_load_formset = LineLoadFormSet(
                queryset=LineLoadModel.objects.none(), prefix="lineload"
            )

            water_table_form = WaterTableForm(prefix="watertable")
            limits_form = LimitsForm(prefix="limits")
            options_form = AnalysisOptionsForm(prefix="options")

            slope = Slope(angle=45)
            slope.set_materials(Material())
            slope.update_analysis_options(iterations=500, slices=10)
            slope.analyse_slope(max_fos=5)

            for s in slope._search:

                c_x = s["c_x"]
                c_y = s["c_y"]
                radius = s["radius"]
                r_c = s["r_c"]
                l_c = s["l_c"]

                # generate points for circle, generates points only along bottom half of circle
                x, y = utilities.generate_circle_coordinates(c_x, c_y, radius)

                # empty vectors for circle points that we will actually include
                x_ = []
                y_ = []

                # 65 long list but the last half of points are for the top half of
                # circle and so will never actually be required.
                for i in range(len(x)):
                    # x coordinate should be between left and right
                    # note for y, should be less than left y but can stoop
                    # below right i
                    if x[i] <= r_c[0] and x[i] >= l_c[0]:
                        x_.append(x[i])
                        y_.append(y[i])

                s["x"] = [l_c[0]] + x_ + [r_c[0]]
                s["y"] = [l_c[1]] + y_ + [r_c[1]]

            search = slope._search

            plot_json = (
                slope.plot_critical().update_layout(height=1200, width=2000).to_json()
            )

            request.session["search"] = search
            request.session["plot_json"] = plot_json
            request.session["forms"] = request.POST

        return render(
            request,
            "slope/index.html",
            {
                "plot_json": plot_json,
                "slope_form": slope_form,
                "material_formset": material_formset,
                "udl_formset": udl_formset,
                "line_load_formset": line_load_formset,
                "water_table_form": water_table_form,
                "limits_form": limits_form,
                "options_form": options_form,
                "forms": [
                    ("Slope", slope_form, "form"),
                    ("Materials", material_formset, "formset"),
                    ("Udls", udl_formset, "formset"),
                    ("LineLoads", line_load_formset, "formset"),
                    ("WaterTable", water_table_form, "form"),
                    ("Limits", limits_form, "form"),
                    ("Options", options_form, "form"),
                ],
                "search": search,
                "COLOUR_FOS_DICT": COLOUR_FOS_DICT,
            },
        )

    elif request.method == "POST":
        # initialize form objects with POST information

        slope_form = SlopeForm(request.POST, prefix="slope")

        material_formset = MaterialFormSet(request.POST, prefix="material")
        udl_formset = UdlFormSet(request.POST, prefix="udl")
        line_load_formset = LineLoadFormSet(request.POST, prefix="lineload")

        water_table_form = WaterTableForm(request.POST, prefix="watertable")
        limits_form = LimitsForm(request.POST, prefix="limits")
        options_form = AnalysisOptionsForm(request.POST, prefix="options")

        form_list = [
            slope_form,
            material_formset,
            udl_formset,
            line_load_formset,
            water_table_form,
            limits_form,
            options_form,
        ]

        # check is valid
        valid = True
        for a in form_list:
            valid *= a.is_valid()

        # if form is valid
        if valid:

            slope = create_slope(*form_list)

            # return color_dictionary
            # add coordinates of failure planes to information that gets passed back.
            for s in slope._search:

                c_x = s["c_x"]
                c_y = s["c_y"]
                radius = s["radius"]
                r_c = s["r_c"]
                l_c = s["l_c"]

                # generate points for circle, generates points only along bottom half of circle
                x, y = utilities.generate_circle_coordinates(c_x, c_y, radius)

                # empty vectors for circle points that we will actually include
                x_ = []
                y_ = []

                # 65 long list but the last half of points are for the top half of
                # circle and so will never actually be required.
                for i in range(len(x)):
                    # x coordinate should be between left and right
                    # note for y, should be less than left y but can stoop
                    # below right i
                    if x[i] <= r_c[0] and x[i] >= l_c[0]:
                        x_.append(x[i])
                        y_.append(y[i])

                s["x"] = [l_c[0]] + x_ + [r_c[0]]
                s["y"] = [l_c[1]] + y_ + [r_c[1]]

            plot = slope.plot_critical(material_table=True, legend=True)
            plot_json = plot.update_layout(autosize=True).to_json()

            search = slope._search

            request.session["search"] = search
            request.session["plot_json"] = plot_json
            request.session["forms"] = request.POST

            return render(
                request,
                "slope/index.html",
                {
                    "plot_json": plot_json,
                    "slope_form": slope_form,
                    "material_formset": material_formset,
                    "udl_formset": udl_formset,
                    "line_load_formset": line_load_formset,
                    "water_table_form": water_table_form,
                    "limits_form": limits_form,
                    "options_form": options_form,
                    "forms": [
                        ("Slope", slope_form, "form"),
                        ("Materials", material_formset, "formset"),
                        ("Udls", udl_formset, "formset"),
                        ("LineLoads", line_load_formset, "formset"),
                        ("WaterTable", water_table_form, "form"),
                        ("Limits", limits_form, "form"),
                        ("Options", options_form, "form"),
                    ],
                    "search": search,
                    "COLOUR_FOS_DICT": COLOUR_FOS_DICT,
                },
            )

    return redirect("reset")


def create_slope(
    slope_form,
    material_formset,
    udl_formset,
    line_load_formset,
    water_table_form,
    limits_form,
    options_form,
):

    # create slope object
    if options_form.cleaned_data["slope_choice"] == "length":
        slope = Slope(
            height=slope_form.cleaned_data["height"],
            length=slope_form.cleaned_data["length"],
        )
    else:
        slope = Slope(
            height=slope_form.cleaned_data["height"],
            length=None,
            angle=slope_form.cleaned_data["angle"],
        )

    # update iterations and slices to consider
    slope.update_analysis_options(
        slices=options_form.cleaned_data["slices"],
        iterations=options_form.cleaned_data["iterations"],
    )

    # add materials to slope
    for material_form in material_formset.cleaned_data:
        if material_form:
            slope.set_materials(
                Material(
                    unit_weight=material_form["unit_weight"],
                    friction_angle=material_form["friction_angle"],
                    cohesion=material_form["cohesion"],
                    depth_to_bottom=material_form["depth_to_bottom"],
                    name=material_form["name"],
                    color=material_form["color"],
                )
            )
        else:
            slope.set_materials(
                Material(
                    unit_weight=MaterialModel._meta.get_field(
                        "unit_weight"
                    ).get_default(),
                    friction_angle=MaterialModel._meta.get_field(
                        "friction_angle"
                    ).get_default(),
                    cohesion=MaterialModel._meta.get_field("cohesion").get_default(),
                    depth_to_bottom=MaterialModel._meta.get_field(
                        "depth_to_bottom"
                    ).get_default(),
                    name=MaterialModel._meta.get_field("name").get_default(),
                    color=MaterialModel._meta.get_field("color").get_default(),
                )
            )

    # add line loads to slope
    for line_load_form in line_load_formset.cleaned_data:
        if line_load_form:
            slope.set_lls(
                LineLoad(
                    magnitude=line_load_form["magnitude"],
                    offset=line_load_form["offset"],
                    color=line_load_form["color"],
                    dynamic_offset=line_load_form["dynamic_offset"],
                )
            )
        else:
            slope.set_lls(
                LineLoad(
                    magnitude=LineLoadModel._meta.get_field("magnitude").get_default(),
                    offset=LineLoadModel._meta.get_field("offset").get_default(),
                    color=LineLoadModel._meta.get_field("color").get_default(),
                    dynamic_offset=LineLoadModel._meta.get_field(
                        "dynamic_offset"
                    ).get_default(),
                )
            )

    # add uniform loads to slope
    for udl_form in udl_formset.cleaned_data:
        if udl_form:
            slope.set_udls(
                Udl(
                    magnitude=udl_form["magnitude"],
                    offset=udl_form["offset"],
                    length=udl_form["length"],
                    color=udl_form["color"],
                    dynamic_offset=udl_form["dynamic_offset"],
                )
            )
        else:
            slope.set_udls(
                Udl(
                    magnitude=UdlModel._meta.get_field("magnitude").get_default(),
                    offset=UdlModel._meta.get_field("offset").get_default(),
                    length=UdlModel._meta.get_field("length").get_default(),
                    color=UdlModel._meta.get_field("color").get_default(),
                    dynamic_offset=UdlModel._meta.get_field(
                        "dynamic_offset"
                    ).get_default(),
                )
            )

    # add water table to slope
    if water_table_form.cleaned_data["consider_water"]:
        slope.set_water_table(water_table_form.cleaned_data["water_depth"])

    # limits form
    limits = limits_form.cleaned_data
    if limits["consider_limits"]:
        if limits["consider_internal_limits"]:
            slope.set_analysis_limits(
                left_x=limits["left_x"],
                right_x=limits["right_x"],
                left_x_right=limits["left_x_right"],
                right_x_left=limits["right_x_left"],
            )
        else:
            slope.set_analysis_limits(
                left_x=limits["left_x"],
                right_x=limits["right_x"],
            )

    if options_form.cleaned_data["analysis_choice"] == "normal":
        slope.analyse_slope(max_fos=5)
    else:

        # might fail if no dynamic loads set up
        try:
            slope.analyse_dynamic(
                critical_fos=options_form.cleaned_data["critical_FOS"]
            )
        except Exception:
            slope.analyse_slope(max_fos=5)

    return slope
