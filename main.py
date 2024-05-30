from clusterization.methods.graph import GraphAlgo
from clusterization.methods.spectr import SpektrAlgo
from clusterization.methods.union import UnionAlgo
from clusterization.data_saver.graph import GraphSaveToExcel
from clusterization.data_saver.spectr import SpectrSaveToExcel
from clusterization.data_saver.union import UnionSaveToExcel

from classification.methods.k_means import KMeans
from classification.methods.parzen_window import ParzenWindow
from classification.methods.standard import Standard
from classification.data_saver.k_means import KMeansSaveToExcel
from classification.data_saver.parzen_window import ParzenWindowSaveToExcel
from classification.data_saver.standard import StandardSaveToExcel

from model.point import Point
from excel_worker.excel_worker import ReadFromExcel
from visual.graphics import ReferenceMethodGraphic, KMeansMethodGraphic, ParzenWindowMethodGraphic
import pandas as pd


def main():
    re = ReadFromExcel()
    re.read('source/first_data.xlsx')
    point_list = []
    for row in re.custom_data_frame.itertuples(index=False):
        point_list.append(Point(id_point=row.id,
                                label=row.class_point,
                                coords=(row.nodes,row.ends),))
        

    g = GraphAlgo(points_dataset=point_list, count_cluster=3)
    g.evalute()



    # Классификация методом эталонов
    # classifier = Standard(zero_point=Point(coords=(5, 3)),
    #                                      dataset = point_list)
    # classifier.evalute()

    # # сохранение в excel
    # we = ReferenceSaveToExcel(classifier.data, re.custom_data_frame)
    # we.save('source/first_data_referernce_algo.xlsx')

    # # отрисовка графика
    # g = ReferenceMethodGraphic(point_list, classifier.data)
    # g.draw()
    
    # Алгоритм кластеризации спектр
    # spk = SpektrAlgo(dataset=point_list, id_start_point=10, count_cluster=3)
    # spk.evalute()

    # we = SpectrSaveToExcel(spk.data, re.custom_data_frame)
    # we.save('source/spectr.xlsx')

    # uni = UnionAlgo(dataset=point_list, count_cluster=3)
    # uni.evalute()

    # we = UnionSaveToExcel(uni.data, re.custom_data_frame)
    # we.save('source/union.xlsx')

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
