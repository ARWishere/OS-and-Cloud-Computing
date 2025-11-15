# andrew welling
# 3 page replacement algorithms
import reference_string


class Page_Replacement:
    def __init__(self, f_size, length=100, local=False):
        self.size = 3
        self.length = length
        gen_string = reference_string.Reference_String()
        if local:
            self.ref_string = gen_string.generate_local(self.length)
        else:
            self.ref_string = gen_string.generate_nonlocal(self.length)

        self.ref_string = [1, 3, 5, 4, 2, 1, 2, 3, 1, 2, 4, 5, 6]

    def FIFO(self):
        # FIFO page replacement algorithm
        page_faults = 0
        pages = []
        for cur_ref in self.ref_string:
            if cur_ref in pages:
                # no page fault if page is loaded
                continue
            if len(pages) == self.size:
                # if full remove page at front
                pages.pop(0)
            pages.append(cur_ref)  # add a new ref
            page_faults += 1  # fault

        return page_faults

    def LRU(self):
        # LRU page replacement algorithm
        page_faults = 0
        pages = {}  # use a dictionary to keep track of when a page was last used by ref string index
        for i, cur_ref in enumerate(self.ref_string):
            if cur_ref in pages:
                pages[cur_ref] = i
                continue
            if len(pages) == self.size:
                # if full remove page least recently used
                lru_page = min(pages, key=pages.get)  # get key with lowest recent usage index
                pages.pop(lru_page)  # remove it
            pages[cur_ref] = i  # add new page
            page_faults += 1  # fault

        return page_faults

    def optimal(self):
        # optimal page replacement algorithm
        page_faults = 0
        pages = []
        for i, cur_ref in enumerate(self.ref_string):
            if cur_ref in pages:
                # do nothing
                continue
            if len(pages) == self.size:
                least_optimal = None
                prev = -1
                for page in pages:
                    try:
                        next = self.ref_string[i + 1:].index(page)
                    except ValueError:  # means page doesnt appear again, so remove it
                        least_optimal = page
                        break
                    if next > prev:  # if the page were scanning is lesser optimal, we want to remove that one
                        prev = next  # update previous
                        least_optimal = page
                pages.remove(least_optimal)
            pages.append(cur_ref)
            page_faults += 1  # fault

        return page_faults
