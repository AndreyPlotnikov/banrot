import csv


class BannerInfo(object):
    """Object which contains info about particular banner"""

    __slots__ = ('url', 'shows', 'categories')

    def __init__(self, url, shows, categories):
        self.url = url
        self.shows = shows
        self.categories = categories

    def __str__(self):
        return '({}, {}, {})'.format(self.url, self.shows, self.categories)


class BanRot(object):
    """This is banners rotation service.
    Be careful, this is not thread-safe implementation!

    :param banners: Banners data. It can be any iterable object.
                    Every item is a tuple of 3 items: (<url>, <number of shows>, <list of categories>)
    """

    def __init__(self, banners):
        self._cat_info = {}
        self._cat_ids = {}
        self._banners = []
        self._all_categories = None
        self.total_iter = 0
        self.num_calls = 0
        cat_id_cnt = 0
        for banner in banners:
            url, shows, categories = banner
            for cat in categories:
                cat_id = self._cat_ids.get(cat)
                if cat_id is None:
                    # add new category
                    cat_id = cat_id_cnt
                    cat_id_cnt += 1
                    self._cat_ids[cat] = cat_id
                cat_info = self._cat_info.get(cat_id)
                if cat_info is None:
                    self._cat_info[cat_id] = cat_info = {'total_shows' : 0}
                # calculating all shows for the category
                cat_info['total_shows'] += shows
            binfo = BannerInfo(url, shows, tuple(self._cat_ids[cat] for cat in categories))
            self._banners.append(binfo)
        self._all_categories = self._cat_ids.values()


    @classmethod
    def from_csv(cls, csv_file, **csv_params):
        """Create and initialize instance from csv file"""
        if isinstance(csv_file, basestring):
            csv_file = open(csv_file)
        reader = csv.reader(csv_file, **csv_params)

        def next_banner():
            for row in reader:
                yield (row[0], int(row[1]), row[2:])

        return cls(next_banner())


    def next_banner(self, categories):
        """Return next banner for given categories.

        :param categories: iterable which contains categories
        :return: banner as BannerInfo instance. If there is no available banners return None
        """
        self.num_calls += 1
        if not categories:
            categories = self._all_categories
        else:
            categories = tuple(self._cat_ids[cat] for cat in categories if cat in self._cat_ids)
        max_shows = -1
        max_cat = None
        # choose a category with largest number of shows
        for cat in categories:
            info = self._cat_info[cat]
            if max_shows < info['total_shows']:
                max_cat = cat
                max_shows = info['total_shows']
            info['total_shows'] -= 1
        choice = None
        num_iter = 0
        for i, banner in enumerate(self._banners):
            num_iter += 1
            if max_cat in banner.categories:
                choice = self._banners.pop(i)
                choice.shows -= 1
                if choice.shows:
                    self._banners.append(choice)
                break
        self.total_iter += num_iter
        if choice is not None:
            # decrease shows counter for each categories in chosen banner
            for cat in choice.categories:
                self._cat_info[cat]['total_shows'] -= 1
        return choice