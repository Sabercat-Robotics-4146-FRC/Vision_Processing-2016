from datetime import datetime
__name__ = "log"
class Log:
    def __init__ ( self, file_name ):
        self.log_file = open( file_name + ".log", "w+")
        msg = "[INIT] initializing log | " + str(datetime.now()) + "\n"
        self.log_file.write( msg )
        print ( msg )
    def write_msg( self, msg, tag ):
        msg = "[" + tag + "] " + msg + " | " + str(datetime.now()) + "\n"
        self.log_file.write( msg )
        print( msg )
    def init( self, msg ):
        self.write_msg( msg, "INIT" )
    def destroy( self, msg ):
        self.write_msg( msg, "DESTROY" )
    def warn( self, msg ):
        self.write_msg( msg, "WARNING" )
    def danger( self, msg ):
        self.write_msg( msg, "DANGER" )
    def debug( self, msg ):
        self.write_msg( msg, "DEBUG" )
    def info( self, msg ):
        self.write_msg( msg, "INFO" )
    def kill( self, msg ):
        self.write_msg( msg, "KILLED")
        self.log_file.close()
