from point import Point
from utilities import ReferenceSaveToExcel, KMeansSaveToExcel, ParzenWindowSaveToExcel, ReadFromExcel
from mmo import ReferenceMethod, KMeans, ParzenWindow, SpektrAlgo
from graphics import ReferenceMethodGraphic, KMeansMethodGraphic, ParzenWindowMethodGraphic
import pandas as pd



def main():
    re = ReadFromExcel()
    re.read('source/first_data.xlsx')
    point_list = []
    for row in re.custom_data_frame.itertuples(index=False):
        point_list.append(Point(id_point=row.id,
                                label=row.class_point,
                                coords=(row.nodes,row.ends),))
    # Классификация методом эталонов
    # classifier = ReferenceMethod(zero_point=Point(coords=(5, 3)),
    #                                      dataset = point_list)
    # classifier.evalute()

    # # сохранение в excel
    # we = ReferenceSaveToExcel(classifier.data, re.custom_data_frame)
    # we.save('source/first_data_referernce_algo.xlsx')

    # # отрисовка графика
    # g = ReferenceMethodGraphic(point_list, classifier.data)
    # g.draw()
    
    spk = SpektrAlgo(dataset=point_list, id_start_point=10, count_cluster=3)
    spk.evalute()
    print('----------------------------------------------------')
    spk.evalute1()

    # # Классификация методом k-means
    # classifier = KMeans(k=5, zero_point=Point(coords=(5, 3)), dataset=point_list)
    # classifier.evalute()

    # we = KMeansSaveToExcel(classifier.data, re.custom_data_frame)
    # we.save('source/first_data_kmeans_algo.xlsx')

    # g = KMeansMethodGraphic(point_list, classifier.data)
    # g.draw()


    # Классификация методом Парзентовского окна
    # classifier = ParzenWindow(radius=4, zero_point=Point(coords=(5, 6)), dataset=point_list)
    # classifier.evalute()
    
    # we = ParzenWindowSaveToExcel(classifier.data, re.custom_data_frame)
    # we.save('source/first_data_parzen_algo.xlsx')

    # g = ParzenWindowMethodGraphic(point_list, classifier.data)
    # g.draw()



    # # ex_d = WorkExcel('source/second_data.xlsx')
    # # point_list = []
    # # for row in ex_d.data_frame.itertuples(index=False):
    # #     point_list.append(Point(id_point=row.id,
    # #                             class_point=row.class_point,
    # #                             coords=[row.z1, row.z2, row.z3],))
    
    # # for point in point_list:
    # #     print(point)

    # # g = Graphic(point_list)
    # # g.draw_3D_graphics()


if __name__ == '__main__':
    main()
