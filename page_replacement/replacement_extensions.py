# andrew welling
# page replacement extensions
# 3 more page replacement algorithms
import page_replacement


class Replacement_Extensions(page_replacement.Page_Replacement):
    def __init__(self, f_size, length=100, local=False):
        super().__init__(f_size, length, local)

    def LFU(self):
        # LFU page replacement algorithm
        page_faults = 0
        pages = {}  # use a dictionary to keep track of page frequency
        for i, cur_ref in enumerate(self.ref_string):
            if cur_ref in pages:
                pages[cur_ref] += 1
                continue
            if len(pages) == self.size:
                # if full remove page least freq used
                lfu_page = min(pages, key=pages.get)  # get key with lowest usage
                pages.pop(lfu_page)  # remove it
            pages[cur_ref] = 1  # add new page with value 1
            page_faults += 1  # fault

        return page_faults

    def MFU(self):
        # MFU page replacement algorithm
        page_faults = 0
        pages = {}  # use a dictionary to keep track of page frequency
        for i, cur_ref in enumerate(self.ref_string):
            if cur_ref in pages:
                pages[cur_ref] += 1
                continue
            if len(pages) == self.size:
                # if full remove page most freq used
                mfu_page = max(pages, key=pages.get)  # get key with highest usage
                pages.pop(mfu_page)  # remove it
            pages[cur_ref] = 1  # add new page with value 1
            page_faults += 1  # fault

        return page_faults

    def inc_dec(self):
        # increments counter for each page by 1 or decrements by 1 depending on page usage
        page_faults = 0
        pages = {}  # use a dictionary to keep track of a counter for each page
        for i, cur_ref in enumerate(self.ref_string):
            if cur_ref in pages:
                pages[cur_ref] += 1  # increment counter since it was used

                # decrement counter of all other pages since they were not used
                for page in pages:
                    if page is not cur_ref:
                        pages[page] -= 1
                continue
            if len(pages) == self.size:
                # if full replace a page
                lowest_page = min(pages, key=pages.get)  # get key with lowest counter
                pages.pop(lowest_page)  # remove it

            # decrement all old pages since they were not used
            for page in pages:
                pages[page] -= 1

            pages[cur_ref] = 0  # add new page w value 0
            page_faults += 1  # fault

        return page_faults
