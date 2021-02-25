def initialize_authority(pages):          #初始化权限向量，一个字典，其中键是url，值都是1
    return dict(zip(pages.keys(), [1]*len(pages)))

def clean_pages(pages):         #删除指向当前正在运行HITS的页面之外的链接
    for page in pages:
        outside_links = []
        for i in range(len(pages[page])):
            if pages[page][i] not in pages or pages[page][i] == page: outside_links.append(i)
        outside_links.reverse()
        for outside_link in outside_links:
            pages[page].pop(outside_link)
    return pages
                
def initialize_L_matrices(pages):
    '''Initializes L, which is just the pages dictionary, and then computes the transpose of L. Matrices are pretty compact since we only store non zero cells.'''
    L_matrix = pages
    Lt_matrix = {}
    for page in pages:
        Lt_matrix[page] = []
    for page in pages:
        for link in pages[page]:
            Lt_matrix[link].append(page)
    return L_matrix, Lt_matrix

def multiply_matrix_vector(matrix, vector):
    '''Multiplies a matrix and a vector'''
    result_matrix = {}
    for row in matrix:
        result_matrix[row] = 0
        for item in matrix[row]:
            result_matrix[row] += vector[item]
    return result_matrix        
            
def normalize(vector):
    '''Takes a vector and divides all components by the component with the max value. This means that the largest value in the vector will be 1.'''
    max = 0
    for component in vector:
        if vector[component] > max:
            max = vector[component]
    if max == 0:
        return vector
    for component in vector:
        vector[component] = float(vector[component]) / max
    return vector
        
def vector_difference(vector1, vector2):
    '''Returns the sum of all of the differences between components in vector1 and vector2.'''
    if not (vector1 and vector2): return float("inf")
    total = 0
    for component in vector1:
        total += abs(vector1[component] - vector2[component])
    return total        

def HITS(pages):
    '''Runs HITS'''
    pages = clean_pages(pages)
    authority_old = None
    authority = initialize_authority(pages)
    (L_matrix, Lt_matrix) = initialize_L_matrices(pages)
    while vector_difference(authority_old, authority) > 0.1:
        authority_old = authority
        hubbiness = normalize(multiply_matrix_vector(L_matrix, authority))
        authority = normalize(multiply_matrix_vector(Lt_matrix, hubbiness))
    return authority, hubbiness

def main():
    '''A simple example of HITS. Page a has links to b and c. Page b links to f. Page c links to b and e. Etc.'''
    pages = {"a":["b", "c"], "b":["f"], "c":["b", "e"], "d":["b"], "e":["c"]}
    (authority, hubbiness) = HITS(pages)
    print("Authority: " + str(authority))
    print("Hubbiness: " + str(hubbiness))

if __name__ == "__main__":
    main()