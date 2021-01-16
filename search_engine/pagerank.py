from search_engine.models import *


class PageRank():
    def __init__(self):
        self.MAX_ITERATIONS = 1000

    def rank(self):
        N = Page.objects.count()
        initial_pr = 1 / N
        Page.objects.update(pagerank=initial_pr)

        for iteration in range(1, self.MAX_ITERATIONS + 1):
            pr_change_sum = 0

            for page in Page.objects.all():
                current_pagerank = page.pagerank
                new_pagerank = 0
                backlink_pages = PageConnect.objects.filter(
                    link=PageLink.objects.filter(url=page.url).first()  #find all urls that have links to the page.url
                )
                for backlink_page in backlink_pages:
                    num = PageLink.objects.filter(url=backlink_page.url).count()
                    if num != 0:
                        new_pagerank += Page(url=backlink_page.url).pagerank / num

                damping_factor = 0.85
                new_pagerank = ((1 - damping_factor) / N) + (damping_factor * new_pagerank)
                Page.objects.filter(url=page.url).update(pagerank=new_pagerank)

                pr_change = abs(new_pagerank - current_pagerank) / current_pagerank
                pr_change_sum += pr_change

            average_pr_change = pr_change_sum / N
            if average_pr_change < 0.0001:
                break