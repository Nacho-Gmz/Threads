# Threads
### Gómez Aldrete Luis Ignacio
### 216588253
#
En esta práctica se piensa ejemplificar de manera muy simple el uso de hilos (*threads*) en Python con la librería *threading*.

El uso de *threads* en programación es importante porque permiten que una aplicación realice múltiples tareas simultáneamente, lo que puede mejorar significativamente su rendimiento y capacidad de respuesta. Los *threads* son unidades independientes de ejecución dentro de un proceso, que pueden ejecutarse de forma concurrente y compartir recursos con otros hilos del mismo proceso. Esto puede permitir que una aplicación realice operaciones de entrada/salida y procesamiento en segundo plano mientras responde a las solicitudes de los usuarios en primer plano, lo que puede mejorar la experiencia del usuario y hacer que la aplicación sea más eficiente.

Para este sencillo ejemplo, las operaciones que se realizarán serán el calculo de cuantas lineas tiene un archivo de texto específico.

Gracias a la función *create_files* dentro de *setup.py* se crean 100 archivos de texto con un número aleatorio de lineas entre 1 y 100.
 ```python
 def create_files():
    for i in range(1, 101):
        filename = f"files/file_{i}.txt"
        with open(filename, "w") as f:
            num_newlines = random.randint(1, 100)
            f.write("\n" * num_newlines)
```

Cada archivo será procesado por la función *process_file*
```python
def process_file(file_path, lock):
    with open(file_path, 'r') as f:
        # read the contents of the file
        contents = f.read()
        
        # count the number of lines in the file
        num_lines = len(contents.split('\n'))
       
        # print the result
        with lock:
            print(f"Processed {file_path}: {num_lines} lines")
```
Y cada instancia de la función *process_file* será convertida en un hilo por la función *process_files* para que se ejecuten de manera paralela.
```python
def process_files(files):
    threads = []
    for file in files:
        t = Thread(target=process_file, args=(file, lock))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
```
Esto hará que cada que se ejecute el programa se configuren 100 *threads* donde cada una se encargará de averiguar cuantas líneas tiene el archivo de texto que le tocó, para luego imprimir su resultado y finalizar su ejecución (la ejecución del *thread*).

Al realizar varias pruebas con este programa, se pudo observar que el orden de finalización de los *threads* dependía hasta cierto punto de cual fue el *thread* que se creo primero, pero a su vez dependía de la cantidad de líneas que el archivo de texto que le tocó al *thread* tenía, pues generalmente los resultados en la terminal llevaban el orden del 1 al 100 con un poco de desorden en algunos puntos.

```
Processed files/file_1.txt: 83 lines
Processed files/file_2.txt: 91 lines
Processed files/file_3.txt: 63 lines
Processed files/file_5.txt: 8 lines
Processed files/file_6.txt: 62 lines
Processed files/file_7.txt: 28 lines
Processed files/file_8.txt: 15 lines
Processed files/file_9.txt: 58 lines
Processed files/file_10.txt: 92 lines
Processed files/file_11.txt: 61 lines
Processed files/file_13.txt: 70 lines
Processed files/file_4.txt: 36 lines
Processed files/file_14.txt: 18 lines
Processed files/file_15.txt: 83 lines
Processed files/file_17.txt: 51 lines
...
```

Por ejemplo, en este fragmento de la salida del programa se puede ver como empieza con *file_1*, *file_2* y *file_3*, pero después se brinca al *file_5* y este cuenta con pocas líneas, por lo que se entiende porque pudo finalizar antes. Sin embargo, el *file_4* no termina hasta 8 archivos después y las 36 líneas con las que cuenta no parecen ser las suficientes como para ameritar una finalización así de tardía, pues la mayoría de archivos entre el *file_5* y *file_4* tienen más líneas que el *file_4*. Una de las razones por la cual este tipo de situaciones sea posible, puede ser el *Lock* que se implementó para que cada *thread* de procesamiento de archivo imprimiese su resultado en una línea sin sobreescribir el resultado de otro *thread*. El *Lock* una especie de turno que comparten todos los *threads* y cada que uno finaliza, revisa si el *Lock* esta desocupado para tomarlo y así imprimir su resultado, mientras no este desocupado, le es imposible imprimir su resultado a pesar de que quizá ya haya finalizado el procesamiento del archivo. 

