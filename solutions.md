Questions and their answers

1. The code is developed and tested and uploaded to a github repository https://github.com/heman2002/RD-Data-Takehome-Himanshu-Singhal

2. The development of the code followed the following process
i) Understanding of the requirements and development of a base project
ii) Identification and coding of the command line parser and its arguments such as dataset file, size, stratification, output file
iii) Parsing the stratification string according to the given format
iv) Once the code required to prepare the data for sampling was ready, the focus shifted to developing the sample data function. There were 2 approaches that were thought of for implementation probabilistic and non-probabilistic. Non-probabilistic method was to use the group by function and achieve individual series of different combinations to select the data from. However, due to the lack of time, I was able to make it work only for a single column and not for multiple columns. This approach guaranteed that the given dataset satisfies the constraints exactly as expected as sampling was done in a non probabilistic manner. The second approach adopted was a probabilistic approach to give weights to each row of the data by multiplying the individual label weights of each column. The weight of the row was then used to select the sampled rows. This approach works to a large extent in choosing the sample data according to constraints, however, being probabilistic in nature may lead to not all the constraints being satified properly.
v) Once the code was developed, proper documentation and test cases were written and it was ensured that edge cases are handled.

Think about:
i) The selection of each row is done using the weight assigned to the row and is done without replacement. This ensures that it is done in an identically distributed and independent manner
ii) If the constraints are not met, a value error is raised stating that the conditions cannot be met.
iii) The weighting of the rows is done in O(nk) time complexity where n is the number of rows and k is the number of columns. An increase in the number of rows will lead to a linear increase in the time complexity slowing down the sampler and the system. This can be handled if the non-probabilistic approach to use group by can be coded, which would lead to time complexity not being influenced by number of columns and system being much faster. Also, the non-probabilistic approach would guarantee all the constraints being achieved.
iv) I would split the code into helper functions and multiple files with further documentation explaining how each component or function works to ensure user-friendliness.
v) The code can be made easily maintainable and scalable by splitting into more files and using concurrency and leveraging multiprocessing workers to perform the sampling for each combination of stratification provided by the user as well as for weighting the different rows.
vi) Unit and Integrated tests have been included in the project to test the functionality for each function as well as the system end to end. The user may encouter issues providing invalid arguments or constraints and the code raises errors when anything is encountered.

If I had more time, I would definitely try to implement the non-probabilistic approach to sampling the data as well as clean up the data.

3. a) There are 2 ways of storing the data if the data was huge. One would be to use a relational database with multiple nodes implemented using sharding where we can shard based upon the stratification column values. This would allow us to sample data very fast as the data will already be in the format that we would require and we can also leverage the power of SQL and indexes for querying and getting the sampled data.  NoSQL can also be used for the meta data for the same reasons if the meta data information changes. A database such as Cassandra with multiple read and write nodes could prove to be ideal for the use case.

The other way is to store the data in a file storage system such as AWS S3 and perform the sampling real-time by reading the meta data files in batches using Apache Hadoop and identifying the samples that satisfy the given constraints and returning them.

b) If the meta data was stored in any type of database, we will need to change the sampler to setup the database connection and write queries to the database and sample the data from the database. If we are storing the data in a file system like S3, we need to write code to setup Hadoop or Spark and develop code to map the stratification constraints and obtain the results by reading through multiple meta data files.