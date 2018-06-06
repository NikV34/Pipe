from django.shortcuts import render, redirect
from .forms import GeometryForm, ConditionForm
import sqlite3
from .models import Geometry


def update_project(col, condition, project_id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("UPDATE thermal_project SET %s=%s WHERE project_id=%s" % (col,condition, project_id))
    conn.commit()
    conn.close()
    return


def index(request):
    print("REQ", request)
    if request.method == "POST":
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        project_list = len(cursor.execute('SELECT * FROM thermal_project').fetchall())
        cursor.execute("INSERT INTO thermal_project (project_id) VALUES (%s)" % project_list)
        conn.commit()
        conn.close()
        return redirect('input-geometry', project_id=project_list)
    return render(request, 'thermal/index.html', locals())


def list_input_data_geometry(project_id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    sektor_list = cursor.execute("SELECT * FROM thermal_geometry where project_id=%s" % project_id).fetchall()
    # cursor.execute("UPDATE thermal_geometry SET %s = %s WHERE sector = %s" % (col, round(value, 2), sec))
    conn.commit()
    conn.close()
    if sektor_list:
        return sektor_list
    else:
        return []


def headline_list_name():
    p = Geometry()
    return p.fields_name()


def interpol(field, value, col):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    min_row = cursor.execute('SELECT * FROM thermal_data WHERE %s <= %s' % (field, value)).fetchall()[-1]
    max_row = cursor.execute('SELECT * FROM thermal_data WHERE %s >= %s' % (field, value)).fetchall()[0]
    # cursor.execute("UPDATE thermal_geometry SET %s = %s WHERE sector = %s" % (col, round(value, 2), sec))
    conn.commit()
    conn.close()
    #print(min_row)
    #print(max_row)
    if min_row == max_row:
        return min_row[col]
    else:
        result = ((max_row[col] - min_row[col]) / (max_row[1] - min_row[1])) * (value - min_row[1]) + min_row[col]
        return result


def input_data_geometry(request, project_id):
    if request.method == "POST":
        form = GeometryForm(request.POST or None)
        if form.is_valid():
            resistance_list = []
            req = request.POST
            post = form.save(commit=False)
            post.total_resistance = 0.0
            if req['skeleton_transcalency'] and req['skeleton_transcalency'] != '0':
                post.skeleton_resistance = float(req['skeleton_thickness']) * 0.001 / float(
                    req['skeleton_transcalency'])
                post.total_resistance += round(post.skeleton_resistance, 2)
            if req['clamp_lining_transcalency'] and req['clamp_lining_transcalency'] != '0':
                post.clamp_lining_resistance = float(req['clamp_lining_thickness']) * 0.001 / float(
                    req['clamp_lining_transcalency'])
                post.total_resistance += round(post.clamp_lining_resistance, 2)
            if req['air_transcalency'] and req['air_transcalency'] != '0':
                post.air_resistance = float(req['air_thickness']) * 0.001 / float(req['air_transcalency'])
                post.total_resistance += round(post.air_resistance, 2)
            if req['insulation_transcalency'] and req['insulation_transcalency'] != '0':
                post.insulation_resistance = float(req['insulation_thickness']) * 0.001 / float(
                    req['insulation_transcalency'])
                post.total_resistance += round(post.insulation_resistance, 2)
            if req['lining_transcalency'] and req['lining_transcalency'] != '0':
                post.lining_resistance = float(req['lining_thickness']) * 0.001 / float(req['lining_transcalency'])
                post.total_resistance += round(post.lining_resistance, 2)
            # print(Geometry.objects.filter(sector='1').exists())
            if post.total_resistance and post.skeleton_resistance:
                if not Geometry.objects.filter(sector=str(post.sector), project_id=str(project_id)).exists():
                    post.project_id = project_id
                    post.save()
    else:
        form = GeometryForm()
    colomns_data = [i[2:-2] for i in list_input_data_geometry(project_id)]
    colomns = len(colomns_data) + 1
    #headline_list = headline_list_name()
    headline_list = ["Номер участка",
                     "Отметка низа, м",
                     "Толщина ствола, мм",
                     "Наружный радиус, мм",
                     "Внутренний радиус, мм",
                     "Теплопров, Вт/(м·°С)",
                     "Терм сопр, м²·°С/Вт",
                     "Толщина п. стенки, мм",
                     "Наружный радиус, мм",
                     "Внутренний радиус, мм",
                     "Теплопров, Вт/(м·°С)",
                     "Терм сопр, м²·°С/Вт",
                     "Толщ в. зазора, мм",
                     "Наружный радиус, мм",
                     "Внутренний радиус, мм",
                     "Теплопров, Вт/(м·°С)",
                     "Терм сопр, м²·°С/Вт",
                     "Толщ теплоизоляции, мм",
                     "Наружный радиус, мм",
                     "Внутренний радиус, мм",
                     "Теплопров, Вт/(м·°С)",
                     "Терм сопр, м²·°С/Вт",
                     "Толщ футеровки, мм",
                     "Наружный радиус, мм",
                     "Внутренний радиус, мм",
                     "Теплопров, Вт/(м·°С)",
                     "Терм сопр, м²·°С/Вт",
                     "Терм сопр стен, м²·°С/Вт"
                    ]
    return render(request, 'thermal/input-data-geometry.html', locals())


def input_data_thermal(request, project_id):
    if request.method == "POST":
        form = ConditionForm(request.POST or None)
        min_temperature = len(list_input_data_geometry(project_id))
        if form.is_valid():
            data = form.cleaned_data
            print('why')
            if data['volume_gas']:
                post = form.save()
                print(post.condition_id)
                update_project('condition_id', post.condition_id, project_id)
                return redirect('result-thermal',
                                project_id=project_id,
                                volume_gas=str(data['volume_gas']),
                                current_temperature_gas=str(data['current_temperature_gas']),
                                current_temperature=str(data['current_temperature'])
                                )
    else:
        form = ConditionForm()
    return render(request, 'thermal/input-data-thermal.html', locals())


def result_thermal(request, project_id, volume_gas, current_temperature_gas, current_temperature):
    result = {}
    count = 1
    bottom_mark = 0
    header = headline_list_name()
    input_list = {'volume_gas': int(volume_gas),
                  'current_temperature_gas': int(current_temperature_gas),
                  'current_temperature': int(current_temperature)
                  }
    for d in list_input_data_geometry(project_id):
        data = d
        result_list = {}
        for i in range(len(header)):
            input_list[header[i]] = data[i]
        min_radius = []
        if input_list['bottom_mark']:
            input_list['current_temperature_gas'] = int(round(input_list['current_temperature_gas']
                                                        - (input_list['bottom_mark'] - bottom_mark) * 0.4, 0))
            bottom_mark = input_list['bottom_mark']
        #print(input_list)
        for radius in [input_list['skeleton_radius_inner'], input_list['clamp_lining_radius_inner'],
                       input_list['air_radius_inner'], input_list['insulation_radius_inner'],
                       input_list['lining_radius_inner']]:
            if radius:
                min_radius.append(radius)
        result_list['inner_diameter'] = 2 * min(min_radius) / 1000
        result_list['cross_area'] = round(result_list['inner_diameter'] * result_list['inner_diameter'] * 3.14 / 4, 2)
        result_list['speed_gas'] = round(input_list['volume_gas'] / result_list['cross_area'], 2)
        result_list['kinematic_viscosity'] = interpol('temperature_gas', input_list['current_temperature_gas'], 3)
        result_list['reynolds_number'] = int(result_list['inner_diameter'] * result_list['speed_gas']
                                             / result_list['kinematic_viscosity'])
        result_list['coefficient_volumetric_expansion'] = 0.00345
        result_list['temperature_difference'] = 1
        result_list['grashof_number'] = int(result_list['coefficient_volumetric_expansion'] * 9.8
                                            * pow(result_list['inner_diameter'], 3)
                                            * result_list['temperature_difference']
                                            / pow(result_list['kinematic_viscosity'], 2))
        result_list['prandtl_number'] = 0.69
        result_list['C'] = 0.135
        result_list['n'] = 0.33333
        result_list['nusselt_number'] = int(round(0.024 * pow(result_list['reynolds_number'], 0.8)
                                                  * pow(result_list['prandtl_number'], 0.35), 0))
        result_list['heat_output_gas'] = interpol('temperature_gas', input_list['current_temperature_gas'], 4)
        result_list['alfa1'] = int(round(result_list['nusselt_number'] * result_list['heat_output_gas']
                                         / result_list['inner_diameter'], 0))
        result_list['alfa2'] = int(round(5 + 10 * pow(result_list['speed_gas'], 0.5), 0))
        result_list['total_resistance_all'] = round(1 / result_list['alfa1'] + 1 / result_list['alfa2']
                                                    + input_list['total_resistance'], 5)
        if input_list['lining_resistance']:
            result_list['lining_inner_temperature'] = round(input_list['current_temperature_gas']
                                                            - (input_list['current_temperature_gas']
                                                               - input_list['current_temperature'])
                                                            * (1 / result_list['alfa1'])
                                                            / result_list['total_resistance_all'], 1)
            result_list['lining_outer_temperature'] = round(result_list['lining_inner_temperature']
                                                            - (input_list['current_temperature_gas']
                                                               - input_list['current_temperature'])
                                                            * input_list['lining_resistance']
                                                            / result_list['total_resistance_all'], 1)
        else:
            result_list['lining_inner_temperature'] = round(float(input_list['current_temperature_gas']), 1)
            result_list['lining_outer_temperature'] = result_list['lining_inner_temperature']
        if not input_list['insulation_resistance']:
            input_list['insulation_resistance'] = 0
        if not input_list['air_resistance']:
            input_list['air_resistance'] = 0
        result_list['clamp_lining_inner_temperature'] = round(result_list['lining_outer_temperature']
                                                              - (input_list['current_temperature_gas']
                                                                 - input_list['current_temperature'])
                                                              * (input_list['insulation_resistance']
                                                                 + input_list['air_resistance'])
                                                              / result_list['total_resistance_all'], 1)
        if input_list['clamp_lining_resistance']:
            result_list['clamp_lining_outer_temperature'] = round(result_list['clamp_lining_outer_temperature']
                                                                  - (input_list['current_temperature_gas']
                                                                     - input_list['current_temperature'])
                                                                  * input_list['clamp_lining_resistance']
                                                                  / result_list['total_resistance_all'], 1)
        else:
            result_list['clamp_lining_outer_temperature'] = result_list['clamp_lining_inner_temperature']
        result_list['skeleton_inner_temperature'] = result_list['clamp_lining_outer_temperature']
        result_list['skeleton_outer_temperature'] = round(result_list['skeleton_inner_temperature']
                                                          - (input_list['current_temperature_gas']
                                                             - input_list['current_temperature'])
                                                          * input_list['skeleton_resistance']
                                                          / result_list['total_resistance_all'], 1)
        result[count] = result_list
        result[count]['sector'] = input_list['sector']
        result[count]['bottom_mark'] = input_list['bottom_mark']
        count += 1
    headline_result = ['Номер участка',
                       'Отметка низа, м',
                       'Температура несущего ствола снаружи, °С',
                       'Температура несущего ствола внутри, °С',
                       'Температура прижимной кладки снаружи, °С',
                       'Температура прижимной кладки внутри, °С',
                       'Температура футеровки снаружи, °С',
                       'Температура футеровки внутри, °С'
                       ]
    result_colomn = {}
    for key, value in result.items():
        result_colomn[key] = [value['sector'],
                              value['bottom_mark'],
                              value['skeleton_outer_temperature'],
                              value['skeleton_inner_temperature'],
                              value['clamp_lining_outer_temperature'],
                              value['clamp_lining_inner_temperature'],
                              value['lining_outer_temperature'],
                              value['lining_inner_temperature'],
                              ]
    #update_project('result_id', post.condition_id, project_id)
    return render(request, 'thermal/result-thermal.html', locals())
