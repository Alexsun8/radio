
allowDiffSec = 2  # allowable differance in sec
freq = 44100 # частота сэмплирования
framesInSecond = 210  # todo - примерное количество фреймов в секунду
allowDiffFrame = allowDiffSec * framesInSecond  # allowable differance in frames

Examplepath1 = "data/test/PodShkvOgnem.mp3"
# Examplepath2 = "data/test/CUTPodShkvOgnem.mp3"  # он наинается примерно с 21700-21710, первое норм совпадение - 21712, однако до того 35576 - отловить еиничное???
Examplepath2 = "data/test/Chernovik.mp3"
DEFAULT_CONFIG_FILE = "/home/alexsun8/streamlabs/radio/hashes/dejavu/dejavu.cnf.SAMPLE" # cfg of dejavu
# DEFAULT_CONFIG_FILE = "hashes/dejavu/dejavu.cnf.SAMPLE" # cfg of dejavu

# эмпирические значения:
closeIndexes = 40 # в какой окрестности индексы считаются близкими, 2этап, поиск первой точки
num_for_check_if_not_collision = 8 # колиество индексо поряд, которые нужно набрать
diffForFirstAndNext = 5 * num_for_check_if_not_collision # окретность, в которой считается, что хеш увеличивает счетчик, а не становится новым возможным первым
hashes_diff = 40 # определение окрестности различий для 3 этапа
tenSec = framesInSecond * 10 # количество фреймов в 10 секундах
