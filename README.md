# Homo Invidens
## Программные компоненты и библиотеки, необходимые для запуска программы:

1. [Python 3.* Toolkit](https://www.python.org/downloads/) - в состав которого входит интерпретатор языка,   
консоль для запуска приложений .py, программная оболочка для просмотра кода и менеджер пакетов pip3.

2. Библиотеки: (последовательнотсь действий для запуска программного кода будет изложена в следующем подзаголовке)
  1. scipy
  2. matplotlib 
  3. math
  4. pandas

## Последоватетльность действий для запуска программного кода:

1. Установка Python 3.* Toolkit - по ссылке выше.
2. Установка библиотек с помощью pip3 в составе Toolkit'а:
  * Для Windows команда cmd: C:\your\path\to\pip3.exe install <lib_name>
  * Для Linux команда bash: sudo C:\your\path\to\pip3.exe install <lib_name>
  * Пример пути: "C:\Python34\Tools\Scripts\pip3.exe install numpy"

  * В соответствии с вашей ОС запустить команду: pip3 install libs.txt

3. Программа рассчитана на корректные входные данные.  
   Условия входных данных:  
   V0 >= 0  
   m > 0  
   h > 0  
  Файлы **Wind.csv** и **F.csv** должны лежать в одной директории с **main.py**, **integrate_method.py**, **digit_method.py**.

  Файлы **Wind.csv**, **F.csv** должны начинаться со шапки (пример: "Height (m),Wx (m/s),Wz (m/s)", "V(m/s),F(N)")
  Разделители в **.csv** файлах - запятые 
  Последовательность столбцов в **Wind.csv**: Высота (метры), Проекция скорости ветра на Ох (м/с), Проекция скорости ветра на Оz (м/с)
  Последовательность столбцов в **F.csv**: Скорость (м/с), Аэродинамическая сила на нем(Н)

4. После того, как все компоненты загружены, запустить файл **main.py** 
и следовать инструкциям в консоли.

## Логика мат. модели

Т.к обеспечить попадание можно изменением только начальных координат, без изменения угла, угол принимаем за 0.  
Саму мат. модель можно представить в виде системы дифферинциальных уравнений.



## Логика программы

В программе реализованы два метода нахождения координат и скорости тела в зависимости от времени. 

В методе **digit_method** мы рассматриваем небольшие участки времени. В течение каждого такого участка мы принимаем, что сила, 
действующая на тело, постоянна, и рассматриваем равноускоренное дижение. Этот метод устойчив, но неточен, а при малых элементарных 
участках времени он работает слишком долго.

В методе **integrate_method** мы решаем систему дифференциальных уравнений с помощью готовой библиотеки. Этот метод точнее предыдущего, 
но неустойчивее. При некоторых входных данных с какого-то момента просчёта траектории все выдаваемые значения начинают зануляться,
из-за особенностей библиотеки

В итоге: программа вначале использует метод **integrate_method**; если он сработал правильно, то она выводит его результат, нет - 
запускает **digit_method** и выводит его результат.
