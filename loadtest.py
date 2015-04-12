import random
import uuid
import time
import core

num_iterations = 10000
categories = ['cat{}'.format(i+1) for i in range(10)]


def timeit(func, repeat):
    t0 = time.time()
    while repeat > 0:
        func()
        repeat -= 1
    return time.time() - t0


def gen_random_categories(num_cats=None, avail_cats=None):
    if avail_cats is None:
        avail_cats = categories[:]
    if num_cats is None:
        num_cats = random.randrange(1, len(avail_cats))
    cats = []
    while num_cats > 0:
        i = random.randrange(len(avail_cats))
        cats.append(avail_cats.pop(i))
        num_cats -= 1
    return cats


def run_test(name, get_banner):
    def gen_banners():
        n = 1000
        while n > 0:
            yield get_banner(n)
            n -= 1

    banrot = core.BanRot(gen_banners())

    def nextBanner():
        cats = gen_random_categories()
        banner = banrot.next_banner(cats)
        #print banner

    t = timeit(nextBanner, num_iterations)
    print '[{}] complete: total time: {:.2f}; per call: {:.5f}'.format(
        name, t, t / num_iterations)


def test_avg_cat_dispersion():
    def get_banner(n):
        url = 'http://localhost/images/' + str(uuid.uuid4())
        shows = 10
        cats = tuple(gen_random_categories())
        return (url, shows, cats)

    run_test('Average dispersion', get_banner)


def test_rare_cat():

    def get_banner(n):
        url = 'http://localhost/images/' + str(uuid.uuid4())
        shows = 10
        if n == 500:
            cats = tuple(gen_random_categories(None, categories[:9])) + (categories[9],)
        else:
            cats = tuple(gen_random_categories(None, categories[:9]))
        return (url, shows, cats)

    run_test('One rare category', get_banner)


def test_most_rare_cats():

    def get_banner(n):
        url = 'http://localhost/images/' + str(uuid.uuid4())
        shows = 10
        if n >= 500 and n < 500 + len(categories) - 2:
            cats = tuple(gen_random_categories(None, categories[:2])) + (categories[2 + n - 500],)
        else:
            cats = tuple(gen_random_categories(None, categories[:2]))
        return (url, shows, cats)

    run_test('Majority categories are rare', get_banner)


if __name__ == '__main__':
    test_avg_cat_dispersion()
    test_rare_cat()
    test_most_rare_cats()
