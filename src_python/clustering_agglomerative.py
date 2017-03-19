import collection_reader
import plot_util
import preprocessing_util
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity

if __name__ == "__main__":
    # Read data
    books = collection_reader.read_books_from_mongo();
    documents = collection_reader.extract_corpus(books)
    print("{} books:".format(len(documents)))
    print([book["book_id3"] for book in books])
    print()

    # Create term-document representation
    X = preprocessing_util.convert_to_term_document(documents, min_df=0.1, max_df=0.9)

    # SVD
    X = preprocessing_util.apply_svd(X, min(X.shape))

    # Cosine similarity matrix
    dist = 1 - cosine_similarity(X)

    ###############################################################################
    # Do the actual clustering
    k = 4

    # linkage: ward, average, complete
    # affinity: cosine, euclidean, cityblock
    ac = AgglomerativeClustering(linkage="average", n_clusters=k, affinity="cosine")

    print("Clustering sparse data with {}".format(ac))
    t0 = time()
    # ac.fit(X.todense())
    ac.fit(dist)
    print("done in {}".format(time() - t0))
    print()

    print("Cluster results:")
    print(ac.labels_)

    # Create a 3d scatter plot of the corpus
    plot_util.create_3d_plot_for_sparse_matrix(X, ac.labels_)
