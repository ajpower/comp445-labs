from threading import Lock


class FileManagerLock:
    """Reader/Writer lock with multiple Reader and priority to Writer
    """
    def __init__(self):
        self.block_reader = Lock()
        self.block_writer = Lock()
        self.writer_count = 0
        self.mutex_writer_count = Lock()
        self.reader_count = 0
        self.mutex_reader_count = Lock()

    def read_acquire(self):
        """Queues up a reader.
        Proceeds if no writer is waiting or writing
        """
        # No Reader will proceed if writers are in line or writing
        with self.block_reader:
            with self.mutex_reader_count:
                self.reader_count += 1
                # Block writers if this is the first reader in queue
                if self.reader_count == 1:
                    self.block_writer.acquire()

    def read_release(self):
        """Releases a reader.
        """
        with self.mutex_reader_count:
            self.reader_count -= 1
            # Release writer's block if this is the last reader reading
            if self.reader_count == 0:
                self.block_writer.release()

    def write_acquire(self):
        """Queues up a writer.
         Will prevent further reader or writer from queueing up
         """
        with self.mutex_writer_count:
            self.writer_count += 1
            # Block further reader from proceeding if this is the first writer in line
            if self.writer_count == 1:
                self.block_reader.acquire()
        # Only 1 writer at a time
        self.block_writer.acquire()

    def write_release(self):
        """Release a writer.
        Priority will be given to queued up writer
        """
        # Let other writer go through
        self.block_writer.release()
        with self.mutex_writer_count:
            self.writer_count -= 1
            # Release reader block if this is the last writer in line
            if self.writer_count == 0:
                self.block_reader.release()
