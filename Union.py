#Coding=UTF-8
import UrlCrawler
import FounderCrawler
import FollowerCrawler
import ReplicatorCrawler
import threading

def main():
    UrlCrawler.UrlCrawlerMethod()
    threads = []
    t1 = threading.Thread(target = FounderCrawler.FounderCrawlerMethod)
    t2 = threading.Thread(target = FollowerCrawler.FollowerCrawlerMethod)
    t3 = threading.Thread(target = ReplicatorCrawler.ReplicatorCrawlerMethod)
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    for i in range(0,3):
        threads[i].start()
    for i in range(0, 3):
        threads[i].join()
    print('\n\nAll down.\n')

if __name__=="__main__":
    main()



