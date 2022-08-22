import arxiv
import hashlib

def get_query_url(cats : list):
    purl = "http://export.arxiv.org/api/query?search_query="
    for a in cats[:-1]:
        purl += "cat:"+ a + "+OR+"
    purl += "cat:"+cats[-1]
    purl += "&id_list=&sortBy=submittedDate&sortOrder=descending&start="
    return purl

def get_result_list(cats : list,start,max_cnt) -> list:
    res_l = []

    page_url = get_query_url(cats)+str(start)+"&max_results="+str(max_cnt)
    feed = arxiv.Client()._parse_feed(page_url, 1)

    for entry in feed.entries:
        res_l.append( arxiv.Result._from_feed_entry(entry) )

    return res_l

def get_entry_hash(entry : arxiv.Result):
    hashstr = entry.title + entry.summary
    hashed_string = hashlib.sha256(hashstr.encode('utf-8')).hexdigest()
    return (hashed_string)

def get_article_title(id_art):
    search = arxiv.Search(id_list=[id_art])
    paper = next(search.results())
    return paper.title

def download_pdf(id_art,dir,fname):
    search = arxiv.Search(id_list=[id_art])
    paper = next(search.results())
    paper.download_pdf(dirpath=dir, filename=fname)