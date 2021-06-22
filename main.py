from hashes.hashing import hashing
from parse_CMD import parse_cmd
from cfg import Examplepath1, Examplepath2, allowDiffFrame, DEFAULT_CONFIG_FILE, num_for_check_if_not_collision, \
    diffForFirstAndNext, hashes_diff, tenSec, framesInSecond, sameCoef
import matplotlib.pyplot as plt
import numpy as np

import soundfile as sf


def compareHashes(BasehashesArr, NewhashesArr, fr_ptr1, printGraph, pointsDiff=None):
    """
    Определяет, является ли фрагмент частью эталонного
    :param BasehashesArr: массив эталоннных хешей
    :param NewhashesArr: массив хешей фрагмента
    :param fr_ptr: первое совпадение с учётом коллизий
    :return: True - в случае совпадения, None - в обратном
    """
    fr_ptr = fr_ptr1
    if fr_ptr1 == -1:
        fr_ptr = 0

    diffLen = 0  # счетчик количества не найденных и/или коллизий.
    # При достижении порога allowDiffFrame, функция возвращает отрицательный рзультат
    firstInd = NewhashesArr.index(BasehashesArr[fr_ptr])
    ind = firstInd
    fp = fr_ptr

    for frameHash in NewhashesArr[firstInd:]:

        allow_diff = allowDiffFrame

        # if allow_diff < diffLen: #todo delete
        #     allow_diff = diffLen

        if len(BasehashesArr) - fr_ptr - 1 < allow_diff:
            allow_diff = len(BasehashesArr) - fr_ptr - 1

        if frameHash in BasehashesArr[
                        fr_ptr - 1:fr_ptr + allow_diff]:
            tempInd = BasehashesArr.index(frameHash, fr_ptr - 1, fr_ptr + allow_diff)

            if tempInd - fr_ptr <= diffLen + hashes_diff and tempInd + 600 >= ind:  # 600 - примерно 2 сек шума, доработать!!!
                fr_ptr = BasehashesArr.index(frameHash, fr_ptr - 1, fr_ptr + allow_diff)
                diffLen = 0

            else:
                diffLen += 1

        else:
            diffLen += 1

        if diffLen >= allowDiffFrame:  # todo return
            if printGraph:
                t1 = np.arange(0, len(pointsDiff), 1)
                plt.plot(t1, pointsDiff, 'k')
                plt.plot(fp, 0, 'ro')
                plt.savefig(printGraph)
                plt.show()
            return None, tempInd - diffLen

        ind += 1

        if printGraph:
            pointsDiff.append(diffLen)

    if printGraph:
        t1 = np.arange(0, len(pointsDiff), 1)
        plt.plot(t1, pointsDiff, 'k')
        if fr_ptr1 == -1:
            plt.plot(fp, 0, 'ro')
        else:
            plt.plot(fp, 0, 'go')
        plt.savefig(printGraph)
        plt.show()

    return True, len(NewhashesArr) - 1


def compare(pathBase=Examplepath1, pathNew=Examplepath2, printGraph=None):
    """
    Сравнивает 2 mp3 файла. Рассчитно, что оба файла моно, в обратном случае учитывается только 1 канал.

    :param pathBase: эталонный файл
    :param pathNew: фрагмент, который ищем в эталонном
    :return: выводит в консоль "THE SAME. IT'S OKEY." в случае совпадения и "DIFFERENT!!!" - в случае различия.
    """
    # for frame in openStream(path2): #todo dinamic iteration without saving

    '''
    Узнаем длительность звуковых фрагментов
    '''
    # soundNew = sf.SoundFile(pathNew)
    # newTime = len(soundNew) / soundNew.samplerate

    BasehashesArr, baseTimeArr = hashing(pathBase,
                                         DEFAULT_CONFIG_FILE)  # хеширования файлов, сохранения в единый массив
    NewhashesArr, newTimeArr = hashing(pathNew, DEFAULT_CONFIG_FILE)

    print(f'len of hashes Array ЦРВ {len(BasehashesArr)}')

    # frInSecNew = len(NewhashesArr) / newTime

    # eigenvector = []  # заккоментированный код позволяет вывести индексы совпадений
    # ind_vec = []
    # for i, hsh in enumerate(NewhashesArr):
    #     if hsh in BasehashesArr:
    #         eigenvector.append(BasehashesArr.index(hsh))
    #         ind_vec.append(i)
    #     else:
    #         eigenvector.append('-')
    #
    # print(eigenvector)
    # print(ind_vec[2:50])

    prop_dict = {}  # {prop_first_point : num_of_next_elems} Словарь с возможными первыми точками в качестве ключа,
    # и с количеством след. точек в области в качестве значения
    ind_dict = {}  # индексы возможных первых точек
    lastNearPoint = {}  # словарь с последней точкой окрестности

    pointsDiff = None
    if printGraph:
        pointsDiff = []

    diff = 0  # количество не найденных подряд хешей
    first_point = None  # вычисленная 1 точка
    for frameHash in NewhashesArr:

        if frameHash in BasehashesArr[:tenSec]:
            ''' 
            При нахождени совпадения хеша кадра из искомого фрагмента с каким-то хешом из эталонного трека, производится
            проверка по всем сохраненным возможным первым точкам. Если сопадение находится в окрестности одной из первых
            точек, оно увеличивает счётчик, тем самым показывая, что сопадение не единственное, образует некую 
            возрастающую последовательность индексов. 
            В случае коллизии хеши, найденные в других частях произведения, не соберут достаточное количество 
            "последовательных ближайших хешей" 
            '''
            isFirstPoint = True
            frameInd = BasehashesArr.index(frameHash)
            for key in prop_dict:
                if 0 <= frameInd - ind_dict[key] < diffForFirstAndNext:
                    prop_dict[key] += 1
                    lastNearPoint[key] = frameInd
                    isFirstPoint = False
                    if prop_dict[key] >= num_for_check_if_not_collision:
                        first_point = ind_dict[key]
                        break

            if first_point:
                break

            if isFirstPoint:
                prop_dict[frameHash] = 0
                ind_dict[frameHash] = frameInd
                lastNearPoint[frameInd] = frameInd


        else:
            diff += 1
            if diff >= allowDiffFrame:
                break

        if printGraph:
            pointsDiff.append(diff)

    firstInclIndex = 0
    # firstInclIndex = diff

    if first_point:
        if printGraph:
            pointsDiff.append(0)

        res, firstInclIndex = compareHashes(BasehashesArr, NewhashesArr, first_point, printGraph=printGraph,
                                            pointsDiff=pointsDiff)

        if res:
            print("THE SAME. IT'S OKEY.")
            return True, firstInclIndex / framesInSecond
    else:  # todo return
        if printGraph:
            t1 = np.arange(0, len(pointsDiff), 1)
            plt.plot(t1, pointsDiff, 'k')
            plt.savefig(printGraph)
            plt.show()
    # else: #todo delete
    #     if printGraph:
    #         pointsDiff.append(0)

    # res, firstInclIndex = compareHashes(BasehashesArr, NewhashesArr, -1, printGraph=printGraph, pointsDiff=pointsDiff)

    # if res:
    #     print("THE SAME. IT'S OKEY.")
    #     return True, firstInclIndex/210

    print("DIFFERENT!!!")
    print(firstInclIndex, firstInclIndex + diff)
    return False, (firstInclIndex / (210 * 60))


def findFirst(array, indF, numNeeded):
    if len(array) <= indF:
        indF = len(array) - 1
    if array[indF] >= numNeeded:
        while indF >= 0 and array[indF] >= numNeeded:
            indF -= 1
            if indF <= len(array):
                return indF - 1
        return indF - 1

    else:
        while array[indF] < numNeeded:
            indF += 1
        return indF


def findLast(array, indF, numNeeded):
    if len(array) <= indF:
        indF = len(array) - 1
    if array[indF] <= numNeeded:
        while indF <= len(array) and array[indF] <= numNeeded:
            indF += 1
            if indF <= len(array):
                return indF - 1

        return indF - 1

    else:
        while array[indF] > numNeeded:
            indF -= 1
        return indF

def distance(base, sec):
    dist = 0
    for letterBase, letterSec in zip(base, sec):
        if letterBase != letterSec:
            dist += 1

    return dist

def compareSynth(pathBase=Examplepath1, pathNew=Examplepath2, printGraph=None):
    BasehashesArr, baseTimeArr, audRate = hashing(pathBase,
                                                  DEFAULT_CONFIG_FILE)  # хеширования файлов, сохранения в единый массив
    print('base_hashes array is ready')
    NewhashesArr, newTimeArr, audRateNew = hashing(pathNew, DEFAULT_CONFIG_FILE)
    print('new_hashes array is ready')

    print(audRate)
    print(audRateNew)
    breakPoint = 0
    diff = 0
    diffArr = []
    for i, hash in enumerate(NewhashesArr):
        hashTime = newTimeArr[i]

        for baseHash in BasehashesArr[
                   findFirst(baseTimeArr, i, hashTime - 20): (findLast(baseTimeArr, i, hashTime + 20) + 1)]:
            if distance(baseHash, hash)<len(hash)*sameCoef:
                diff = 0
                if i < 40000:
                    breakPoint = i
                break
        else:
            diff += 1

        diffArr.append(diff)

    print('DIFF array and comparing is ready')

    print(f'"Секунд" в ролике: {newTimeArr[len(newTimeArr)-1]}')
    if printGraph:
        # print()
        t1 = np.arange(0, len(diffArr), 1)
        #     t1 = np.arange(0,5000, 1)
        plt.plot(t1, diffArr, 'k')
        # plt.plot(t1, diffArr[:5000], 'k')
        plt.savefig(printGraph)
        plt.show()

    print(f'Точка расхождения(номер кадра): {breakPoint}')
    print(f'Точка расхождения(~"секундах"): {newTimeArr[breakPoint]}')
    print(f'всего времени: {newTimeArr[len(newTimeArr) - 1]}')


if __name__ == '__main__':
    # path1, path2, cfgPath, plotPatsh = parse_cmd()  # возвращает путь к эталонному файлу, фрагменту и путь к файлу
    # с настройками
    # compare(path1, path2, printGraph=plotPath)

    compareSynth(
        '/home/alexsun8/streamlabs/radio/data/Список радио сравнения трансляций/7 Радио 7 Рязань ТР-705 '
        '16-59/ЦРВ_РАДИО 7 Ямал 402 11265 V_0d [2021-02-12T16_59_00..2021-02-12T17_02_00].ts',
        '/home/alexsun8/streamlabs/radio/data/Список радио сравнения трансляций/7 Радио 7 Рязань ТР-705 '
        '16-59/АРВ_Радио 7_1f [2021-02-12T16_59_00..2021-02-12T17_02_00].ts',
        './temPlot.png')
