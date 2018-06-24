# threading-skillup
## Threading-1
In **threading-1.mai** you can find a simple example of running 5 threads. Each of them is displaying number and log them to
the file **threading-1.log** after ending of loop - thread is sleeping. You can see in logs file, that threads are displaying
data in parallel. Also in logs file you can see the comparison of multithreading display perfomance and running the same
in one thread.
So, as we can see in logs file -  multithreading displaying is faster, why? Because it is I/O task and each iteration there
are call of "sleep" function. I/O in unix is working the same(for example networking, working with files and etc.)
## Threading-2
In **threading-2.main** you can find a simple example of using threads in fetching data via http. There are 3 different approaches -
multithreading with lock, multithreading without lock and just in main thread. Each approach is calling fetch_url function
5 times. So, as a result, we have 5*WEATHER_API_CITY_ID_LIST GET requests to third party weather API. All logs for program
you can find in threading-2.log file. This code shows, that multithreading is a good approach, for example, when we need to get data
from several API's, then do something with this data and return results to user. Also, in this code is used locks. Lock is ability
to avoid issues with critical sections. Let's imagine: you got the media file  and you need to write the content of file
chunk by chunk, but because of some reasons other 4 users also got the media files and we need to put whole this content into
one file. To make content holistic we need to set the lock, then write  chunks of first user into file and then release this lock to
other thread, which write chunks of other user. Also working with lock is a little bit faster, because we are reducing the count of context switching, but the difference
is not so big like amount of time for doing the same without thr eads.