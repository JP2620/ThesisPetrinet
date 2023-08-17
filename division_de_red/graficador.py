from PIL import Image
import os
import subprocess
import json

def json_to_dot_with_title(json_data, title):
    edges_dict = {}
    node_states = {}
    for edge in json_data['edges']:
        from_node = edge['from']
        to_node = edge['to']
        transition = edge['path'].split('(')[1].split(')')[0]
        edges_dict[(from_node, to_node)] = transition

    for node in json_data['nodes']:
        node_id = node['id']
        state = node['state']
        node_states[node_id] = state

    dot_representation = f'digraph G {{\n  label="{title}";\n'
    for node, state in node_states.items():
        dot_representation += f'  {node} [label="{node}\\n{state}"];\n'
    for edge, transition in edges_dict.items():
        dot_representation += f'  {edge[0]} -> {edge[1]} [label="{transition}"];\n'
    dot_representation += '}'

    return dot_representation

def process_json_files(json_files):
    images = []
    for json_file in json_files:
        with open(json_file, 'r') as file:
            json_data = json.load(file)
        
        # Título para el grafo DOT (nombre del archivo sin extensión)
        title = os.path.basename(json_file).split('.')[0]
        
        # Convertir JSON a DOT
        dot_data = json_to_dot_with_title(json_data, title)
        
        # Crear archivo DOT
        dot_file_path = f'./salida/{title}.dot'
        with open(dot_file_path, 'w') as file:
            file.write(dot_data)
        
        # Crear PNG usando el comando dot
        png_file_path = f'./salida/{title}.png'
        subprocess.run(['dot', '-Tpng', dot_file_path, '-o', png_file_path])
        
        # Abrir la imagen PNG
        image = Image.open(png_file_path)
        images.append(image)

    return images

def create_grid(images, grid_size=(3, 3), image_size=(300, 300), line_width=5):
    # Crear una imagen vacía para contener la cuadrícula
    total_width = (image_size[0] + line_width) * grid_size[0] + line_width
    total_height = (image_size[1] + line_width) * grid_size[1] + line_width
    grid_image = Image.new('RGB', (total_width, total_height), 'black')

    # Iterar a través de las imágenes y colocarlas en la cuadrícula
    for i, image in enumerate(images):
        # Escalar la imagen
        scaled_image = image.resize(image_size, Image.ANTIALIAS)
        # Calcular la posición en la cuadrícula
        row = i // grid_size[0]
        col = i % grid_size[0]
        x = col * (image_size[0] + line_width) + line_width
        y = row * (image_size[1] + line_width) + line_width
        # Pegar la imagen en la cuadrícula
        grid_image.paste(scaled_image, (x, y))

    return grid_image

import sys

def main():
    # Asegurarse de que se proporcione al menos un archivo JSON
    if len(sys.argv) < 2:
        print("Uso: python graficador.py <json_file1> <json_file2> ...")
        sys.exit(1)

    # Lista de archivos JSON a procesar
    json_files = sys.argv[1:]

    # Procesar los archivos JSON y obtener las imágenes
    images = process_json_files(json_files)

    # Definir el tamaño de la cuadrícula y el tamaño individual de la imagen
    grid_size = (len(images), 1) # Ajustar según sea necesario
    image_size = (400, 400) # Tamaño individual de la imagen

    # Crear la cuadrícula con las imágenes
    grid_image = create_grid(images, grid_size, image_size)

    # Opcionalmente, guardar la imagen de la cuadrícula en un archivo
    grid_image_path = './salida/grid_image.png'
    grid_image.save(grid_image_path)

if __name__ == "__main__":
    main()
