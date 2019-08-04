# Data Engineering Pipeline with Apache Airflow

python TEST_stage_redshift_operator.py run start 2019-08-03


airflow test TEST_sparkify_dag prepare_redshift 2019-08-03;

airflow test TEST_sparkify_dag stage_events_to_redshift 2019-08-03;

airflow test TEST_sparkify_dag stage_songs_to_redshift 2019-08-03;

airflow test TEST_sparkify_dag load_user_dimension_table 2019-08-03;

airflow test TEST_sparkify_dag load_songplays_fact_table_task 2019-08-03;


## References

https://medium.com/@shahnewazk/dockerizing-airflow-58a8888bd72d

https://medium.com/datareply/airflow-lesser-known-tips-tricks-and-best-practises-cf4d4a90f8f


## Set Up

### Local Docker Containers


## Amazon Web Services (AWS) Set Up

Amazon Web Services is the primary technology platform for this solution. Instructions for set up
and execution of the PostgreSQL prototype are included at the end of this document.


### AWS Redshift Cluster

Follow the normal Redshift cluster creation documentation available on AWS with the addition of using
an `Elastic IP` for the publicly exposed IP address. The `Elastic IP` helps with diagnosing
configuration problems.

The steps for create a new Redshift cluster are generally:

1. Click "Launch cluster"
2. Enter unique cluster identifier and "sparkify" for database name and master username
3. Enter and confirm master username password
4. Click "Continue"
5. Select node type and create 2 node multi-node cluster
6. Click "Continue"
7. Select default VPC and default subnet group
8. Select "Choose a public IP address" and select an existing Elastic IP
9. Click "Continue"
10. Review settings and click "Launch cluster"

Ensure that port 5439 is open on the VPC Security Group that is assigned
to the cluster. With this configuration the Redshift cluster may accessed using a normal desktop
database client (like DbVisualizer).


## Extra: Containerizing Airflow

https://airflow.apache.org/start.html

https://medium.com/@shahnewazk/dockerizing-airflow-58a8888bd72d



## Extra: Copy Project's Workspace

    zip -r workspace.zip workspace
    mv workspace.zip workspace_original.zip
    mv workspace_original.zip workspace
