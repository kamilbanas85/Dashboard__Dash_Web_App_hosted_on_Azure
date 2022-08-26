####################################################
####################################################

if __name__ == '__main__':
    
    sched1 = BackgroundScheduler(daemon=True)
    if not sched1.running: # Clause suggested by @CyrilleMODIANO

        sched1.add_job(Download_Process_And_Save_Data, 'interval', minutes=5,\
                       args = [Authenication, False, True, FolderWithData])
        sched1.start()
        
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: sched1.shutdown(wait=False))
    
    # To print opend jobs in sheduler
    # for job in sched1.get_jobs():
    #   print("name: %s, trigger: %s, next run: %s, handler: %s" % (
    #     job.name, job.trigger, job.next_run_time, job.func))
    
    
    
    dash_app.run_server(debug=True, use_reloader=False)


#############################################################
#############################################################
#############################################################


if __name__ == '__main__':
    
    # when using the reloder, there are master and child process, Your scheduler thread runs in both. You need to prevent the scheduler from running in the master process 
    if not app.debug or os.envir.get('WEKZEUG_RUN_MAIN') == 'true':
        sched1 = BackgroundScheduler(daemon=True)
        if not sched1.running:
        
            sched1.add_job(Download_Process_And_Save_Data, 'interval', minutes=5,\
                           args = [Authenication, False, True, FolderWithData])      
            # , misfire_grace_time = None
            sched1.start()
    
    # shut down the scheduler when exiting the app
    atexit.register(lambda: sched1.shutdown(wait = False))

    
    dash_app.run_server(debug=True, use_reloader = False)