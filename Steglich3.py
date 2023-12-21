def calculate_centroid(vertices):
    x_sum = sum(v[0] for v in vertices)
    y_sum = sum(v[1] for v in vertices)
    z_sum = sum(v[2] for v in vertices)
    num_vertices = len(vertices)
    centroid = [x_sum / num_vertices, y_sum / num_vertices, z_sum / num_vertices]
    return centroid

def move_vertices(obj_file, sentence):
    vertices = []
    faces = []

    with open(obj_file, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = [float(coord) for coord in line.strip().split()[1:]]
                vertices.append(vertex)
            elif line.startswith('f '):
                face = [index for index in line.strip().split()[1:]]
                faces.append(face)

    if len(vertices) < len(sentence):
        print("Not enough vertices in the OBJ file for the given sentence.")
        return
    print("vertices in obj", len(vertices))
    fraction = 0.001
    centroid = calculate_centroid(vertices)

    for i, char in enumerate(sentence):
        ascii_val = ord(char) * fraction
        vertex = vertices[i]
        displacement = [val - centroid[idx] for idx, val in enumerate(vertex)]
        displaced_vertex = [val + (displacement[idx] * ascii_val) for idx, val in enumerate(vertex)]
        vertices[i] = displaced_vertex

    new_obj_file = obj_file.split('.')[0] + '_decrypt.obj'

    with open(new_obj_file, 'w') as file:
        for vertex in vertices:
            file.write(f"v {' '.join(str(coord) for coord in vertex)}\n")

        for face in faces:
            file.write(f"f {' '.join(str(index) for index in face)}\n")

    print(f"Modified OBJ file saved as {new_obj_file}")

def extract_message(original_obj_file, modified_obj_file):
    original_vertices = []
    modified_vertices = []

    with open(original_obj_file, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = [float(coord) for coord in line.strip().split()[1:]]
                original_vertices.append(vertex)

    with open(modified_obj_file, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = [float(coord) for coord in line.strip().split()[1:]]
                modified_vertices.append(vertex)

    if len(original_vertices) != len(modified_vertices):
        print("The number of vertices in the original and modified files do not match.")
        return ""

    extracted_message = ''

    for orig_vertex, mod_vertex in zip(original_vertices, modified_vertices):
        displacement = [mod_val - orig_val for mod_val, orig_val in zip(mod_vertex, orig_vertex)]
        displacement_mag = sum(val ** 2 for val in displacement) ** 0.5
        closest_ascii_val = round(displacement_mag / 0.001)
        if closest_ascii_val != 0:
            extracted_message += chr(int(closest_ascii_val))

    return extracted_message



# Replace 'input.obj' with the path to your OBJ file
input_obj_file = 'n.obj'


# Replace 'hello' with your input sentence
input_sentence_1 = 'Privacy is crucial in the digital era for an open society - not secrecy, but selectively revealing oneself. Transactions should share only necessary info - anonymitys vital. Cypherpunks advocate for anonymous systems, oppose encryption regulations, and defend privacy through code. For privacy to flourish, societal agreement is key. Eric Hughes hughes@soda.berkeley.edu 9 March 1993 K i t K P i d d w E a x n h e r N D k u B p C G u N K o M E Z h w Z k G D R Q s e T k I V e H S S'
input_sentence = input()
print("len of sentence", len(input_sentence))
move_vertices(input_obj_file, input_sentence)

# Usage example:
# Replace 'input_modified.obj' with the path to your modified OBJ file
extracted = extract_message('n.obj', 'n_decrypt.obj')
print("Extracted message:", extracted)