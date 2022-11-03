from tokenize import group
import pandas as pd
import pdfplumber
from os import path
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import re
from scrapper import get_table


oven_power_list_40, oven_power_list_08, induction_power_value, microwave_power_cost = (
    [],
    [],
    [],
    [],
)  #
electricty_price_df = get_table("https://www.stimatracker.com/historic")
unit_price = float(electricty_price_df["DC2"][0])


def get_power(power_list):
    app_voltage, app_current, app_cost = [], [], []
    for i in range(len(power_list)):
        a = re.split("/", power_list[i])
        for voltage in re.findall(r"-?\d+\.?\d*", a[0]):
            app_voltage.append(float(voltage))
        for current in re.findall(r"-?\d+\.?\d*", a[2]):
            app_current.append(float(current))
        app_temp = round((app_current[i] * app_voltage[i]) / 1000 * unit_price, 2)
        app_cost.append(app_temp)
    return app_cost


file_path = path.realpath("catalogue/Samsung_2018.pdf")
with pdfplumber.open(file_path) as temp:
    # Oven
    item_title = temp.pages[30].extract_text()
    first_page = temp.pages[31].extract_table()
    oven_df = pd.DataFrame.from_dict(first_page)
    power = oven_df.loc[17]
    model = oven_df.loc[0]
    power_list = [power.iloc[i] for i in range(len(power)) if i > 0]
    for i in range(len(power_list)):
        if i > 0:
            power_one = power.iloc[i]
            actual_power = re.split("\n", power_one)
            # 240V
            # global dict_40
            usable_power_40 = re.split("/", actual_power[0])
            test_power_40 = [usable_power_40[1]]
            for j in test_power_40:
                for s in re.findall(r"-?\d+\.?\d*", j):
                    oven_power_list_40.append(float(s))

            # 208V
            global dict_08
            usable_power_08 = re.split("/", actual_power[1])
            test_power_08 = [usable_power_08[1]]
            for j in test_power_08:
                for s in re.findall(r"-?\d+\.?\d*", j):
                    cost_temp = float(s) * unit_price
                    oven_power_list_08.append(float(s))
                dict_08 = {"208V": oven_power_list_08}
    # Induction ovens
    induction_page = temp.pages[33].extract_table()
    induction_df = pd.DataFrame.from_dict(induction_page)
    induction_power = induction_df.loc[10]
    induction_model = induction_df.loc[0]
    induction_power_list = [
        induction_power.iloc[i] for i in range(len(induction_power)) if i > 0
    ]
    for k in induction_power_list:
        for val in re.findall(r"-?\d+\.?\d*", k):
            induction_power_value.append(float(val))
            # Oven
            oven_power_cost_08 = [round(unit_price * i, 2) for i in oven_power_list_08]

    # Microwaves(range)
    microwave_page = temp.pages[64].extract_table()
    microwave_df = pd.DataFrame.from_dict(microwave_page)
    microwave_model = microwave_df.loc[0]
    microwave_power = microwave_df.loc[4]
    microwave_power_list = [
        microwave_power.iloc[i] for i in range(len(microwave_power)) if i > 0
    ]
    for m_power in microwave_power_list[2:]:
        for val in re.findall(r"-?\d+\.?\d*", m_power):
            m_test_cost = round(float(val) / 1000 * unit_price, 2)
            microwave_power_cost.append(m_test_cost)

    # Dishwasher
    dishwasher_page = temp.pages[79].extract_table()
    dishwasher_df = pd.DataFrame.from_dict(dishwasher_page)
    dishwasher_model = dishwasher_df.loc[0]
    dishwasher_power = dishwasher_df.loc[4]
    dishwasher_power_list = [
        dishwasher_power.iloc[i] for i in range(len(dishwasher_power)) if i > 0
    ]
    # Fridge
    fridge_page = temp.pages[103].extract_table()
    fridge_page_2 = temp.pages[105].extract_table()
    fridge_page_3 = temp.pages[107].extract_table()
    fridge_page_4 = temp.pages[109].extract_table()
    freezer_page = temp.pages[111].extract_table()
    fridge_df = pd.DataFrame.from_dict(fridge_page)
    fridge_df_2 = pd.DataFrame.from_dict(fridge_page_2)
    fridge_df_3 = pd.DataFrame.from_dict(fridge_page_3)
    fridge_df_4 = pd.DataFrame.from_dict(fridge_page_4)
    freezer_df = pd.DataFrame.from_dict(freezer_page)
    fridge_model = fridge_df.loc[0]
    fridge_model_2 = fridge_df_2.loc[0]
    fridge_model_3 = fridge_df_3.loc[0]
    fridge_model_4 = fridge_df_4.loc[0]
    freezer_model = freezer_df.loc[0]
    fridge_power = fridge_df.loc[15]
    fridge_power_2 = fridge_df_2.loc[16]
    fridge_power_3 = fridge_df_3.loc[17]
    fridge_power_4 = fridge_df_4.loc[14]
    freezer_power = freezer_df.loc[10]
    fridge_power_list = [
        fridge_power.iloc[i] for i in range(len(fridge_power) - 1) if i > 0
    ]

    global fridge_1_power
    fridge_1_power = get_power(fridge_power_list)
    fridge_power_list_2 = [
        fridge_power_2.iloc[i] for i in range(len(fridge_power_2)) if i > 0
    ]
    global fridge_2_power
    fridge_2_power = get_power(fridge_power_list_2)

    fridge_power_list_3 = [
        fridge_power_3.iloc[i] for i in range(len(fridge_power_3) - 1) if i > 0
    ]
    global fridge_3_power
    fridge_3_power = get_power(fridge_power_list_3)

    fridge_power_list_4 = [
        fridge_power_4.iloc[i] for i in range(len(fridge_power_4)) if i > 0
    ]
    global fridge_4_power
    fridge_4_power = get_power(fridge_power_list_4)
    freezer_power_list = [
        freezer_power.iloc[i] for i in range(len(freezer_power)) if i > 0
    ]

    global freezer_cost
    freezer_cost = get_power(freezer_power_list)

    # Washing machine Front load
    washing_front_page = temp.pages[130].extract_table()
    washing_front_df = pd.DataFrame.from_dict(washing_front_page)
    washing_front_power = washing_front_df.loc[28]
    washing_front_model = washing_front_df.loc[0]
    washing_front_power_list = [
        washing_front_power.iloc[i] for i in range(len(washing_front_power)) if i > 0
    ]
    global washing_front_cost
    washing_front_cost = get_power(washing_front_power_list)

    # Washing machine Top load
    washing_top_table = temp.pages[132].find_tables()
    washing_top_temp = temp.pages[132].extract_table()
    washing_top_model = washing_top_temp[0]
    washing_top_page = washing_top_table[1].extract()
    washing_top_df = pd.DataFrame.from_dict(washing_top_page)
    washing_top_power = washing_top_df.loc[5]
    washing_top_power_list = [
        washing_top_power.iloc[i] for i in range(len(washing_top_power)) if i > 0
    ]
    global washing_top_cost
    washing_top_cost = get_power(washing_front_power_list)

# Washing machine
washing_front_list = [
    {"Name": "Washing Machine Front-Load", "Model": a, "Cost": b}
    for (a, b) in zip(washing_front_model[1:], washing_front_cost[:-1])
]
washing_top_list = [
    {"Name": "Washing Machine Top-Load", "Model": a, "Cost": b}
    for (a, b) in zip(washing_top_model[1:], washing_top_cost)
]
washing_front_pd = pd.DataFrame.from_dict(washing_front_list)
washing_top_pd = pd.DataFrame.from_dict(washing_top_list)

# Fridge
fridge_list = [
    {"Name": "Fridge 4-Door Flex", "Model": a, "Cost": b}
    for (a, b) in zip(fridge_model[1:], fridge_1_power)
]

fridge_list_2 = [
    {"Name": "Fridge 4-Door French Door", "Model": a, "Cost": b}
    for (a, b) in zip(fridge_model_2[1:], fridge_2_power)
]
fridge_list_3 = [
    {"Name": "Fridge 3-Door French Door", "Model": a, "Cost": b}
    for (a, b) in zip(fridge_model_3[1:], fridge_3_power)
]
fridge_list_4 = [
    {"Name": "Fridge Side-by-Side", "Model": a, "Cost": b}
    for (a, b) in zip(fridge_model_4[1:], fridge_4_power)
]
freezer_list = [
    {"Name": "Freezer", "Model": a, "Cost": b}
    for (a, b) in zip(freezer_model[1:], freezer_cost)
]
freezer_pd = pd.DataFrame.from_dict(freezer_list)
fridge_dict = fridge_list + fridge_list_2 + fridge_list_3 + fridge_list_4
fridge_pd = pd.DataFrame.from_dict(fridge_dict)


# Microwave(range)
microwave_dict = [
    {"Name": "Microwave", "Model": a, "Cost": b}
    for (a, b) in zip(microwave_model[1:], microwave_power_cost)
]
microwave_cost = pd.DataFrame.from_dict(microwave_dict)


# Oven
oven_power_cost_08 = [round(unit_price * i, 2) for i in oven_power_list_08]
oven_power_cost_40 = [round(unit_price * i, 2) for i in oven_power_list_40]

oven_power_dict = [
    {"Name": "Oven", "Model": a, "208V": b, "240V": c}
    for (a, b, c) in zip(model[1:], oven_power_cost_08, oven_power_cost_40)
]
oven_pd = pd.DataFrame.from_dict(oven_power_dict)

# Induction
induction_power_cost = [round(unit_price * i, 2) for i in induction_power_value]
induction_dict = [
    {"Name": "Induction Oven", "Model": a, "Cost": b}
    for (a, b) in zip(induction_model[1:], induction_power_cost)
]
induction_pd = pd.DataFrame.from_dict(induction_dict)


pd_list = [
    induction_pd,
    microwave_cost,
    washing_front_pd,
    washing_top_pd,
    freezer_pd,
    fridge_pd,
]
final_pd = pd.concat(pd_list)
final_pd.insert(3, "Usage", [1 for _ in range(len(final_pd["Cost"]))])

# Dash
app = Dash(__name__)
colors = {"background": "white", "text": "rgba(176,136,27,1)"}
app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.Div(
            children=[
                html.H2(
                    "Visualisation of Energy Costs per appliance model",
                    style={"textAlign": "center", "color": colors["text"]},
                )
            ]
        ),
        dcc.Graph(
            id="appliance-graph",
            responsive=True,
        ),
        html.H4("Appliance", style={"color": colors["text"], "textAlign": "center"}),
        dcc.Dropdown(
            [
                "Oven",
                "Induction Oven",
                "Microwave",
                "Washing Machine Front-Load",
                "Washing Machine Top-Load",
                "Freezer",
                "Fridge 4-Door French Door",
                "Fridge 3-Door French Door",
                "Fridge Side-by-Side",
                "Fridge 4-Door Flex",
            ],
            value="Oven",
            id="app-type",
            style={"width": "70%", "margin": "auto"},
        ),
        html.Br(),
        html.Div(
            style={"color": colors["text"]},
            children=[
                html.H5(
                    "Electrity price statistics:https://www.stimatracker.com/historic"
                ),
                html.H5(
                    "Samsung 2018 catalogue source:https://image-us.samsung.com/SamsungUS/samsungbusiness/samsung-builder/pdfs/Samsung_Home_Appliances_2018_Product_Catalog.pdf"
                ),
                html.H6(
                    "Last updated on 3rd November 2022", style={"textAlign": "center"}
                ),
            ],
        ),
    ],
)


@app.callback(Output("appliance-graph", "figure"), Input("app-type", "value"))
def update_graph(app_name):
    new_df = final_pd[final_pd["Name"] == app_name]
    if app_name == "Oven":
        fig = px.bar(
            oven_pd,
            x=oven_pd["Model"],
            y=[oven_pd["208V"], oven_pd["240V"]],
            barmode="group",
        )
    else:
        # new_df["Usage"] = {hour_usage}
        fig = px.bar(
            new_df, x="Model", y="Cost", labels={"Cost": "Cost of usage(ksh./kWh)"}
        )
    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )
  