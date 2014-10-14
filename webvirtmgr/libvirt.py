#
# WARNING WARNING WARNING WARNING
#
# This file is automatically written by generator.py. Any changes
# made here will be lost.
#
# To change the manually written methods edit libvirt-override.py
# To change the automatically written methods edit generator.py
#
# WARNING WARNING WARNING WARNING
#
#
# Manually written part of python bindings for libvirt
#

# On cygwin, the DLL is called cygvirtmod.dll
import sys

try:
    import libvirtmod
except ImportError:
    lib_e = sys.exc_info()[1]
    try:
        import cygvirtmod as libvirtmod
    except ImportError:
        cyg_e = sys.exc_info()[1]
        if str(cyg_e).count("No module named"):
            raise lib_e

import types

# The root of all libvirt errors.
class libvirtError(Exception):
    def __init__(self, defmsg, conn=None, dom=None, net=None, pool=None, vol=None):

        # Never call virConnGetLastError().
        # virGetLastError() is now thread local
        err = libvirtmod.virGetLastError()
        if err is None:
            msg = defmsg
        else:
            msg = err[2]

        Exception.__init__(self, msg)

        self.err = err

    def get_error_code(self):
        if self.err is None:
            return None
        return self.err[0]

    def get_error_domain(self):
        if self.err is None:
            return None
        return self.err[1]

    def get_error_message(self):
        if self.err is None:
            return None
        return self.err[2]

    def get_error_level(self):
        if self.err is None:
            return None
        return self.err[3]

    def get_str1(self):
        if self.err is None:
            return None
        return self.err[4]

    def get_str2(self):
        if self.err is None:
            return None
        return self.err[5]

    def get_str3(self):
        if self.err is None:
            return None
        return self.err[6]

    def get_int1(self):
        if self.err is None:
            return None
        return self.err[7]

    def get_int2(self):
        if self.err is None:
            return None
        return self.err[8]

#
# register the libvirt global error handler
#
def registerErrorHandler(f, ctx):
    """Register a Python function for error reporting.
       The function is called back as f(ctx, error), with error
       being a list of information about the error being raised.
       Returns 1 in case of success."""
    return libvirtmod.virRegisterErrorHandler(f,ctx)

def openAuth(uri, auth, flags=0):
    ret = libvirtmod.virConnectOpenAuth(uri, auth, flags)
    if ret is None:raise libvirtError('virConnectOpenAuth() failed')
    return virConnect(_obj=ret)


#
# Return library version.
#
def getVersion (name = None):
    """If no name parameter is passed (or name is None) then the
    version of the libvirt library is returned as an integer.

    If a name is passed and it refers to a driver linked to the
    libvirt library, then this returns a tuple of (library version,
    driver version).

    If the name passed refers to a non-existent driver, then you
    will get the exception 'no support for hypervisor'.

    Versions numbers are integers: 1000000*major + 1000*minor + release."""
    if name is None:
        ret = libvirtmod.virGetVersion ()
    else:
        ret = libvirtmod.virGetVersion (name)
    if ret is None: raise libvirtError ("virGetVersion() failed")
    return ret


#
# Invoke an EventHandle callback
#
def _eventInvokeHandleCallback(watch, fd, event, opaque, opaquecompat=None):
    """
    Invoke the Event Impl Handle Callback in C
    """
    # libvirt 0.9.2 and earlier required custom event loops to know
    # that opaque=(cb, original_opaque) and pass the values individually
    # to this wrapper. This should handle the back compat case, and make
    # future invocations match the virEventHandleCallback prototype
    if opaquecompat:
        callback = opaque
        opaque = opaquecompat
    else:
        callback = opaque[0]
        opaque = opaque[1]

    libvirtmod.virEventInvokeHandleCallback(watch, fd, event, callback, opaque)

#
# Invoke an EventTimeout callback
#
def _eventInvokeTimeoutCallback(timer, opaque, opaquecompat=None):
    """
    Invoke the Event Impl Timeout Callback in C
    """
    # libvirt 0.9.2 and earlier required custom event loops to know
    # that opaque=(cb, original_opaque) and pass the values individually
    # to this wrapper. This should handle the back compat case, and make
    # future invocations match the virEventTimeoutCallback prototype
    if opaquecompat:
        callback = opaque
        opaque = opaquecompat
    else:
        callback = opaque[0]
        opaque = opaque[1]

    libvirtmod.virEventInvokeTimeoutCallback(timer, callback, opaque)

def _dispatchEventHandleCallback(watch, fd, events, cbData):
    cb = cbData["cb"]
    opaque = cbData["opaque"]

    cb(watch, fd, events, opaque)
    return 0

def _dispatchEventTimeoutCallback(timer, cbData):
    cb = cbData["cb"]
    opaque = cbData["opaque"]

    cb(timer, opaque)
    return 0

def virEventAddHandle(fd, events, cb, opaque):
    """
    register a callback for monitoring file handle events

    @fd: file handle to monitor for events
    @events: bitset of events to watch from virEventHandleType constants
    @cb: callback to invoke when an event occurs
    @opaque: user data to pass to callback

    Example callback prototype is:
        def cb(watch,   # int id of the handle
               fd,      # int file descriptor the event occurred on
               events,  # int bitmap of events that have occurred
               opaque): # opaque data passed to eventAddHandle
    """
    cbData = {"cb" : cb, "opaque" : opaque}
    ret = libvirtmod.virEventAddHandle(fd, events, cbData)
    if ret == -1: raise libvirtError ('virEventAddHandle() failed')
    return ret

def virEventAddTimeout(timeout, cb, opaque):
    """
    register a callback for a timer event

    @timeout: time between events in milliseconds
    @cb: callback to invoke when an event occurs
    @opaque: user data to pass to callback

    Setting timeout to -1 will disable the timer. Setting the timeout
    to zero will cause it to fire on every event loop iteration.

    Example callback prototype is:
        def cb(timer,   # int id of the timer
               opaque): # opaque data passed to eventAddTimeout
    """
    cbData = {"cb" : cb, "opaque" : opaque}
    ret = libvirtmod.virEventAddTimeout(timeout, cbData)
    if ret == -1: raise libvirtError ('virEventAddTimeout() failed')
    return ret
#
# WARNING WARNING WARNING WARNING
#
# Automatically written part of python bindings for libvirt
#
# WARNING WARNING WARNING WARNING
#
# Functions from module libvirt
#

def open(name=None):
    """This function should be called first to get a connection to the
    Hypervisor and xen store
    
    If @name is None, if the LIBVIRT_DEFAULT_URI environment variable is set,
    then it will be used. Otherwise if the client configuration file
    has the "uri_default" parameter set, then it will be used. Finally
    probing will be done to determine a suitable default driver to activate.
    This involves trying each hypervisor in turn until one successfully opens.
    
    If connecting to an unprivileged hypervisor driver which requires
    the libvirtd daemon to be active, it will automatically be launched
    if not already running. This can be prevented by setting the
    environment variable LIBVIRT_AUTOSTART=0
    
    URIs are documented at http://libvirt.org/uri.html """
    ret = libvirtmod.virConnectOpen(name)
    if ret is None:raise libvirtError('virConnectOpen() failed')
    return virConnect(_obj=ret)

def openReadOnly(name=None):
    """This function should be called first to get a restricted connection to the
    library functionalities. The set of APIs usable are then restricted
    on the available methods to control the domains.
    
    See virConnectOpen for notes about environment variables which can
    have an effect on opening drivers
    
    URIs are documented at http://libvirt.org/uri.html """
    ret = libvirtmod.virConnectOpenReadOnly(name)
    if ret is None:raise libvirtError('virConnectOpenReadOnly() failed')
    return virConnect(_obj=ret)

def virEventRegisterDefaultImpl():
    """Registers a default event implementation based on the
    poll() system call. This is a generic implementation
    that can be used by any client application which does
    not have a need to integrate with an external event
    loop impl.
    
    Once registered, the application has to invoke virEventRunDefaultImpl() in
    a loop to process events.  Failure to do so may result in connections being
    closed unexpectedly as a result of keepalive timeout.  The default
    event loop fully supports handle and timeout events, but only
    wakes up on events registered by libvirt API calls such as
    virEventAddHandle() or virConnectDomainEventRegisterAny(). """
    ret = libvirtmod.virEventRegisterDefaultImpl()
    if ret == -1: raise libvirtError ('virEventRegisterDefaultImpl() failed')
    return ret

def virEventRegisterImpl(addHandle, updateHandle, removeHandle, addTimeout, updateTimeout, removeTimeout):
    """Registers an event implementation, to allow integration
    with an external event loop. Applications would use this
    to integrate with the libglib2 event loop, or libevent
    or the QT event loop.
    
    Use of the virEventAddHandle() and similar APIs require that the
    corresponding handler is registered.  Use of the
    virConnectDomainEventRegisterAny() and similar APIs requires that
    the three timeout handlers are registered.  Likewise, the three
    timeout handlers must be registered if the remote server has been
    configured to send keepalive messages, or if the client intends
    to call virConnectSetKeepAlive(), to avoid either side from
    unexpectedly closing the connection due to inactivity.
    
    If an application does not need to integrate with an
    existing event loop implementation, then the
    virEventRegisterDefaultImpl() method can be used to setup
    the generic libvirt implementation. """
    libvirtmod.virEventRegisterImpl(addHandle, updateHandle, removeHandle, addTimeout, updateTimeout, removeTimeout)

def virEventRemoveHandle(watch):
    """Unregister a callback from a file handle.  This function
    requires that an event loop has previously been registered with
    virEventRegisterImpl() or virEventRegisterDefaultImpl(). """
    ret = libvirtmod.virEventRemoveHandle(watch)
    if ret == -1: raise libvirtError ('virEventRemoveHandle() failed')
    return ret

def virEventRemoveTimeout(timer):
    """Unregister a callback for a timer.  This function
    requires that an event loop has previously been registered with
    virEventRegisterImpl() or virEventRegisterDefaultImpl(). """
    ret = libvirtmod.virEventRemoveTimeout(timer)
    if ret == -1: raise libvirtError ('virEventRemoveTimeout() failed')
    return ret

def virEventRunDefaultImpl():
    """Run one iteration of the event loop. Applications
    will generally want to have a thread which invokes
    this method in an infinite loop.  Furthermore, it is wise
    to set up a pipe-to-self handler (via virEventAddHandle())
    or a timeout (via virEventAddTimeout()) before calling this
    function, as it will block forever if there are no
    registered events.
    
      static bool quit = false;
    
      while (!quit) {
        if (virEventRunDefaultImpl() < 0)
          ...print error...
      } """
    ret = libvirtmod.virEventRunDefaultImpl()
    if ret == -1: raise libvirtError ('virEventRunDefaultImpl() failed')
    return ret

def virEventUpdateHandle(watch, events):
    """Change event set for a monitored file handle.  This function
    requires that an event loop has previously been registered with
    virEventRegisterImpl() or virEventRegisterDefaultImpl().
    
    Will not fail if fd exists. """
    libvirtmod.virEventUpdateHandle(watch, events)

def virEventUpdateTimeout(timer, timeout):
    """Change frequency for a timer.  This function
    requires that an event loop has previously been registered with
    virEventRegisterImpl() or virEventRegisterDefaultImpl().
    
    Setting frequency to -1 will disable the timer. Setting the frequency
    to zero will cause it to fire on every event loop iteration.
    
    Will not fail if timer exists. """
    libvirtmod.virEventUpdateTimeout(timer, timeout)

#
# Functions from module virterror
#

def virGetLastError():
    """Provide a pointer to the last error caught at the library level
    
    The error object is kept in thread local storage, so separate
    threads can safely access this concurrently. """
    ret = libvirtmod.virGetLastError()
    return ret

def virGetLastErrorMessage():
    """Get the most recent error message """
    ret = libvirtmod.virGetLastErrorMessage()
    if ret is None: raise libvirtError ('virGetLastErrorMessage() failed')
    return ret

#
# Functions from module libvirt
#

def virInitialize():
    """Initialize the library.
    
    This method is invoked automatically by any of the virConnectOpen() API
    calls, and by virGetVersion(). Since release 1.0.0, there is no need to
    call this method even in a multithreaded application, since
    initialization is performed in a thread safe manner; but applications
    using an older version of the library should manually call this before
    setting up competing threads that attempt virConnectOpen in parallel.
    
    The only other time it would be necessary to call virInitialize is if the
    application did not invoke virConnectOpen as its first API call, such
    as when calling virEventRegisterImpl() before setting up connections,
    or when using virSetErrorFunc() to alter error reporting of the first
    connection attempt. """
    ret = libvirtmod.virInitialize()
    if ret == -1: raise libvirtError ('virInitialize() failed')
    return ret

#
# Functions from module virterror
#

def virResetLastError():
    """Reset the last error caught at the library level.
    
    The error object is kept in thread local storage, so separate
    threads can safely access this concurrently, only resetting
    their own error object. """
    libvirtmod.virResetLastError()

class virDomain(object):
    def __init__(self, conn, _obj=None):
        self._conn = conn
        self._o = _obj

    def __del__(self):
        if self._o is not None:
            libvirtmod.virDomainFree(self._o)
        self._o = None

    def connect(self):
        return self._conn

    #
    # virDomain functions from module libvirt
    #

    def ID(self):
        """Get the hypervisor ID number for the domain """
        ret = libvirtmod.virDomainGetID(self._o)
        return ret

    def OSType(self):
        """Get the type of domain operation system. """
        ret = libvirtmod.virDomainGetOSType(self._o)
        if ret is None: raise libvirtError ('virDomainGetOSType() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def UUID(self):
        """Extract the UUID unique Identifier of a domain. """
        ret = libvirtmod.virDomainGetUUID(self._o)
        if ret is None: raise libvirtError ('virDomainGetUUID() failed', dom=self)
        return ret

    def UUIDString(self):
        """Fetch globally unique ID of the domain as a string. """
        ret = libvirtmod.virDomainGetUUIDString(self._o)
        if ret is None: raise libvirtError ('virDomainGetUUIDString() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def XMLDesc(self, flags=0):
        """Provide an XML description of the domain. The description may be reused
        later to relaunch the domain with virDomainCreateXML().
        
        No security-sensitive data will be included unless @flags contains
        VIR_DOMAIN_XML_SECURE; this flag is rejected on read-only
        connections.  If @flags includes VIR_DOMAIN_XML_INACTIVE, then the
        XML represents the configuration that will be used on the next boot
        of a persistent domain; otherwise, the configuration represents the
        currently running domain.  If @flags contains
        VIR_DOMAIN_XML_UPDATE_CPU, then the portion of the domain XML
        describing CPU capabilities is modified to match actual
        capabilities of the host. """
        ret = libvirtmod.virDomainGetXMLDesc(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetXMLDesc() failed', dom=self)
        return ret

    def abortJob(self):
        """Requests that the current background job be aborted at the
        soonest opportunity. """
        ret = libvirtmod.virDomainAbortJob(self._o)
        if ret == -1: raise libvirtError ('virDomainAbortJob() failed', dom=self)
        return ret

    def attachDevice(self, xml):
        """Create a virtual device attachment to backend.  This function,
        having hotplug semantics, is only allowed on an active domain.
        
        For compatibility, this method can also be used to change the media
        in an existing CDROM/Floppy device, however, applications are
        recommended to use the virDomainUpdateDeviceFlag method instead. """
        ret = libvirtmod.virDomainAttachDevice(self._o, xml)
        if ret == -1: raise libvirtError ('virDomainAttachDevice() failed', dom=self)
        return ret

    def attachDeviceFlags(self, xml, flags=0):
        """Attach a virtual device to a domain, using the flags parameter
        to control how the device is attached.  VIR_DOMAIN_AFFECT_CURRENT
        specifies that the device allocation is made based on current domain
        state.  VIR_DOMAIN_AFFECT_LIVE specifies that the device shall be
        allocated to the active domain instance only and is not added to the
        persisted domain configuration.  VIR_DOMAIN_AFFECT_CONFIG
        specifies that the device shall be allocated to the persisted domain
        configuration only.  Note that the target hypervisor must return an
        error if unable to satisfy flags.  E.g. the hypervisor driver will
        return failure if LIVE is specified but it only supports modifying the
        persisted device allocation.
        
        For compatibility, this method can also be used to change the media
        in an existing CDROM/Floppy device, however, applications are
        recommended to use the virDomainUpdateDeviceFlag method instead. """
        ret = libvirtmod.virDomainAttachDeviceFlags(self._o, xml, flags)
        if ret == -1: raise libvirtError ('virDomainAttachDeviceFlags() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def autostart(self):
        """Extract the autostart flag for a domain """
        ret = libvirtmod.virDomainGetAutostart(self._o)
        if ret == -1: raise libvirtError ('virDomainGetAutostart() failed', dom=self)
        return ret

    def blkioParameters(self, flags=0):
        """Get the blkio parameters """
        ret = libvirtmod.virDomainGetBlkioParameters(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetBlkioParameters() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def blockCommit(self, disk, base, top, bandwidth=0, flags=0):
        """Commit changes that were made to temporary top-level files within a disk
        image backing file chain into a lower-level base file.  In other words,
        take all the difference between @base and @top, and update @base to contain
        that difference; after the commit, any portion of the chain that previously
        depended on @top will now depend on @base, and all files after @base up
        to and including @top will now be invalidated.  A typical use of this
        command is to reduce the length of a backing file chain after taking an
        external disk snapshot.  To move data in the opposite direction, see
        virDomainBlockPull().
        
        This command starts a long-running commit block job, whose status may
        be tracked by virDomainBlockJobInfo() with a job type of
        VIR_DOMAIN_BLOCK_JOB_TYPE_COMMIT, and the operation can be aborted with
        virDomainBlockJobAbort().  When finished, an asynchronous event is
        raised to indicate the final status, and the job no longer exists.  If
        the job is aborted, it is up to the hypervisor whether starting a new
        job will resume from the same point, or start over.
        
        Be aware that this command may invalidate files even if it is aborted;
        the user is cautioned against relying on the contents of invalidated
        intermediate files such as @top without manually rebasing those files
        to use a backing file of a read-only copy of @base prior to the point
        where the commit operation was started (although such a rebase cannot
        be safely done until the commit has successfully completed).  However,
        the domain itself will not have any issues; the active layer remains
        valid throughout the entire commit operation.  As a convenience,
        if @flags contains VIR_DOMAIN_BLOCK_COMMIT_DELETE, this command will
        unlink all files that were invalidated, after the commit successfully
        completes.
        
        By default, if @base is None, the commit target will be the bottom of
        the backing chain; if @flags contains VIR_DOMAIN_BLOCK_COMMIT_SHALLOW,
        then the immediate backing file of @top will be used instead.  If @top
        is None, the active image at the top of the chain will be used.  Some
        hypervisors place restrictions on how much can be committed, and might
        fail if @base is not the immediate backing file of @top, or if @top is
        the active layer in use by a running domain, or if @top is not the
        top-most file; restrictions may differ for online vs. offline domains.
        
        The @disk parameter is either an unambiguous source name of the
        block device (the <source file='...'/> sub-element, such as
        "/path/to/image"), or the device target shorthand (the
        <target dev='...'/> sub-element, such as "xvda").  Valid names
        can be found by calling virDomainGetXMLDesc() and inspecting
        elements within //domain/devices/disk.
        
        The maximum bandwidth (in MiB/s) that will be used to do the commit can be
        specified with the bandwidth parameter.  If set to 0, libvirt will choose a
        suitable default.  Some hypervisors do not support this feature and will
        return an error if bandwidth is not 0; in this case, it might still be
        possible for a later call to virDomainBlockJobSetSpeed() to succeed.
        The actual speed can be determined with virDomainGetBlockJobInfo(). """
        ret = libvirtmod.virDomainBlockCommit(self._o, disk, base, top, bandwidth, flags)
        if ret == -1: raise libvirtError ('virDomainBlockCommit() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def blockInfo(self, path, flags=0):
        """Extract information about a domain block device size """
        ret = libvirtmod.virDomainGetBlockInfo(self._o, path, flags)
        if ret is None: raise libvirtError ('virDomainGetBlockInfo() failed', dom=self)
        return ret

    def blockIoTune(self, disk, flags=0):
        """Get the I/O tunables for a block device """
        ret = libvirtmod.virDomainGetBlockIoTune(self._o, disk, flags)
        if ret is None: raise libvirtError ('virDomainGetBlockIoTune() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def blockJobAbort(self, disk, flags=0):
        """Cancel the active block job on the given disk.
        
        The @disk parameter is either an unambiguous source name of the
        block device (the <source file='...'/> sub-element, such as
        "/path/to/image"), or (since 0.9.5) the device target shorthand
        (the <target dev='...'/> sub-element, such as "xvda").  Valid names
        can be found by calling virDomainGetXMLDesc() and inspecting
        elements within //domain/devices/disk.
        
        If the current block job for @disk is VIR_DOMAIN_BLOCK_JOB_TYPE_PULL, then
        by default, this function performs a synchronous operation and the caller
        may assume that the operation has completed when 0 is returned.  However,
        BlockJob operations may take a long time to cancel, and during this time
        further domain interactions may be unresponsive.  To avoid this problem,
        pass VIR_DOMAIN_BLOCK_JOB_ABORT_ASYNC in the @flags argument to enable
        asynchronous behavior, returning as soon as possible.  When the job has
        been canceled, a BlockJob event will be emitted, with status
        VIR_DOMAIN_BLOCK_JOB_CANCELED (even if the ABORT_ASYNC flag was not
        used); it is also possible to poll virDomainBlockJobInfo() to see if
        the job cancellation is still pending.  This type of job can be restarted
        to pick up from where it left off.
        
        If the current block job for @disk is VIR_DOMAIN_BLOCK_JOB_TYPE_COPY, then
        the default is to abort the mirroring and revert to the source disk;
        adding @flags of VIR_DOMAIN_BLOCK_JOB_ABORT_PIVOT causes this call to
        fail with VIR_ERR_BLOCK_COPY_ACTIVE if the copy is not fully populated,
        otherwise it will swap the disk over to the copy to end the mirroring.  An
        event will be issued when the job is ended, and it is possible to use
        VIR_DOMAIN_BLOCK_JOB_ABORT_ASYNC to control whether this command waits
        for the completion of the job.  Restarting this job requires starting
        over from the beginning of the first phase. """
        ret = libvirtmod.virDomainBlockJobAbort(self._o, disk, flags)
        if ret == -1: raise libvirtError ('virDomainBlockJobAbort() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def blockJobInfo(self, path, flags=0):
        """Get progress information for a block job """
        ret = libvirtmod.virDomainGetBlockJobInfo(self._o, path, flags)
        if ret is None: raise libvirtError ('virDomainGetBlockJobInfo() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def blockJobSetSpeed(self, disk, bandwidth, flags=0):
        """Set the maximimum allowable bandwidth that a block job may consume.  If
        bandwidth is 0, the limit will revert to the hypervisor default.
        
        The @disk parameter is either an unambiguous source name of the
        block device (the <source file='...'/> sub-element, such as
        "/path/to/image"), or (since 0.9.5) the device target shorthand
        (the <target dev='...'/> sub-element, such as "xvda").  Valid names
        can be found by calling virDomainGetXMLDesc() and inspecting
        elements within //domain/devices/disk. """
        ret = libvirtmod.virDomainBlockJobSetSpeed(self._o, disk, bandwidth, flags)
        if ret == -1: raise libvirtError ('virDomainBlockJobSetSpeed() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def blockPeek(self, disk, offset, size, flags=0):
        """Read the contents of domain's disk device """
        ret = libvirtmod.virDomainBlockPeek(self._o, disk, offset, size, flags)
        if ret is None: raise libvirtError ('virDomainBlockPeek() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def blockPull(self, disk, bandwidth=0, flags=0):
        """Populate a disk image with data from its backing image.  Once all data from
        its backing image has been pulled, the disk no longer depends on a backing
        image.  This function pulls data for the entire device in the background.
        Progress of the operation can be checked with virDomainGetBlockJobInfo() and
        the operation can be aborted with virDomainBlockJobAbort().  When finished,
        an asynchronous event is raised to indicate the final status.  To move
        data in the opposite direction, see virDomainBlockCommit().
        
        The @disk parameter is either an unambiguous source name of the
        block device (the <source file='...'/> sub-element, such as
        "/path/to/image"), or (since 0.9.5) the device target shorthand
        (the <target dev='...'/> sub-element, such as "xvda").  Valid names
        can be found by calling virDomainGetXMLDesc() and inspecting
        elements within //domain/devices/disk.
        
        The maximum bandwidth (in MiB/s) that will be used to do the copy can be
        specified with the bandwidth parameter.  If set to 0, libvirt will choose a
        suitable default.  Some hypervisors do not support this feature and will
        return an error if bandwidth is not 0; in this case, it might still be
        possible for a later call to virDomainBlockJobSetSpeed() to succeed.
        The actual speed can be determined with virDomainGetBlockJobInfo().
        
        This is shorthand for virDomainBlockRebase() with a None base. """
        ret = libvirtmod.virDomainBlockPull(self._o, disk, bandwidth, flags)
        if ret == -1: raise libvirtError ('virDomainBlockPull() failed', dom=self)
        return ret

    def blockRebase(self, disk, base, bandwidth=0, flags=0):
        """Populate a disk image with data from its backing image chain, and
        setting the backing image to @base, or alternatively copy an entire
        backing chain to a new file @base.
        
        When @flags is 0, this starts a pull, where @base must be the absolute
        path of one of the backing images further up the chain, or None to
        convert the disk image so that it has no backing image.  Once all
        data from its backing image chain has been pulled, the disk no
        longer depends on those intermediate backing images.  This function
        pulls data for the entire device in the background.  Progress of
        the operation can be checked with virDomainGetBlockJobInfo() with a
        job type of VIR_DOMAIN_BLOCK_JOB_TYPE_PULL, and the operation can be
        aborted with virDomainBlockJobAbort().  When finished, an asynchronous
        event is raised to indicate the final status, and the job no longer
        exists.  If the job is aborted, a new one can be started later to
        resume from the same point.
        
        When @flags includes VIR_DOMAIN_BLOCK_REBASE_COPY, this starts a copy,
        where @base must be the name of a new file to copy the chain to.  By
        default, the copy will pull the entire source chain into the destination
        file, but if @flags also contains VIR_DOMAIN_BLOCK_REBASE_SHALLOW, then
        only the top of the source chain will be copied (the source and
        destination have a common backing file).  By default, @base will be
        created with the same file format as the source, but this can be altered
        by adding VIR_DOMAIN_BLOCK_REBASE_COPY_RAW to force the copy to be raw
        (does not make sense with the shallow flag unless the source is also raw),
        or by using VIR_DOMAIN_BLOCK_REBASE_REUSE_EXT to reuse an existing file
        with initial contents identical to the backing file of the source (this
        allows a management app to pre-create files with relative backing file
        names, rather than the default of absolute backing file names; as a
        security precaution, you should generally only use reuse_ext with the
        shallow flag and a non-raw destination file).
        
        A copy job has two parts; in the first phase, the @bandwidth parameter
        affects how fast the source is pulled into the destination, and the job
        can only be canceled by reverting to the source file; progress in this
        phase can be tracked via the virDomainBlockJobInfo() command, with a
        job type of VIR_DOMAIN_BLOCK_JOB_TYPE_COPY.  The job transitions to the
        second phase when the job info states cur == end, and remains alive to
        mirror all further changes to both source and destination.  The user
        must call virDomainBlockJobAbort() to end the mirroring while choosing
        whether to revert to source or pivot to the destination.  An event is
        issued when the job ends, and depending on the hypervisor, an event may
        also be issued when the job transitions from pulling to mirroring.  If
        the job is aborted, a new job will have to start over from the beginning
        of the first phase.
        
        Some hypervisors will restrict certain actions, such as virDomainSave()
        or virDomainDetachDevice(), while a copy job is active; they may
        also restrict a copy job to transient domains.
        
        The @disk parameter is either an unambiguous source name of the
        block device (the <source file='...'/> sub-element, such as
        "/path/to/image"), or the device target shorthand (the
        <target dev='...'/> sub-element, such as "xvda").  Valid names
        can be found by calling virDomainGetXMLDesc() and inspecting
        elements within //domain/devices/disk.
        
        The maximum bandwidth (in MiB/s) that will be used to do the copy can be
        specified with the bandwidth parameter.  If set to 0, libvirt will choose a
        suitable default.  Some hypervisors do not support this feature and will
        return an error if bandwidth is not 0; in this case, it might still be
        possible for a later call to virDomainBlockJobSetSpeed() to succeed.
        The actual speed can be determined with virDomainGetBlockJobInfo().
        
        When @base is None and @flags is 0, this is identical to
        virDomainBlockPull(). """
        ret = libvirtmod.virDomainBlockRebase(self._o, disk, base, bandwidth, flags)
        if ret == -1: raise libvirtError ('virDomainBlockRebase() failed', dom=self)
        return ret

    def blockResize(self, disk, size, flags=0):
        """Resize a block device of domain while the domain is running.  If
        @flags is 0, then @size is in kibibytes (blocks of 1024 bytes);
        since 0.9.11, if @flags includes VIR_DOMAIN_BLOCK_RESIZE_BYTES,
        @size is in bytes instead.  @size is taken directly as the new
        size.  Depending on the file format, the hypervisor may round up
        to the next alignment boundary.
        
        The @disk parameter is either an unambiguous source name of the
        block device (the <source file='...'/> sub-element, such as
        "/path/to/image"), or (since 0.9.5) the device target shorthand
        (the <target dev='...'/> sub-element, such as "xvda").  Valid names
        can be found by calling virDomainGetXMLDesc() and inspecting
        elements within //domain/devices/disk.
        
        Note that this call may fail if the underlying virtualization hypervisor
        does not support it; this call requires privileged access to the
        hypervisor. """
        ret = libvirtmod.virDomainBlockResize(self._o, disk, size, flags)
        if ret == -1: raise libvirtError ('virDomainBlockResize() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def blockStats(self, path):
        """Extracts block device statistics for a domain """
        ret = libvirtmod.virDomainBlockStats(self._o, path)
        if ret is None: raise libvirtError ('virDomainBlockStats() failed', dom=self)
        return ret

    def blockStatsFlags(self, path, flags=0):
        """Extracts block device statistics parameters of a running domain """
        ret = libvirtmod.virDomainBlockStatsFlags(self._o, path, flags)
        if ret is None: raise libvirtError ('virDomainBlockStatsFlags() failed', dom=self)
        return ret

    def controlInfo(self, flags=0):
        """Extract details about current state of control interface to a domain. """
        ret = libvirtmod.virDomainGetControlInfo(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetControlInfo() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def coreDump(self, to, flags=0):
        """This method will dump the core of a domain on a given file for analysis.
        Note that for remote Xen Daemon the file path will be interpreted in
        the remote host. Hypervisors may require  the user to manually ensure
        proper permissions on the file named by @to.
        
        If @flags includes VIR_DUMP_CRASH, then leave the guest shut off with
        a crashed state after the dump completes.  If @flags includes
        VIR_DUMP_LIVE, then make the core dump while continuing to allow
        the guest to run; otherwise, the guest is suspended during the dump.
        VIR_DUMP_RESET flag forces reset of the quest after dump.
        The above three flags are mutually exclusive.
        
        Additionally, if @flags includes VIR_DUMP_BYPASS_CACHE, then libvirt
        will attempt to bypass the file system cache while creating the file,
        or fail if it cannot do so for the given system; this can allow less
        pressure on file system cache, but also risks slowing saves to NFS. """
        ret = libvirtmod.virDomainCoreDump(self._o, to, flags)
        if ret == -1: raise libvirtError ('virDomainCoreDump() failed', dom=self)
        return ret

    def create(self):
        """Launch a defined domain. If the call succeeds the domain moves from the
        defined to the running domains pools.  The domain will be paused only
        if restoring from managed state created from a paused domain.  For more
        control, see virDomainCreateWithFlags(). """
        ret = libvirtmod.virDomainCreate(self._o)
        if ret == -1: raise libvirtError ('virDomainCreate() failed', dom=self)
        return ret

    def createWithFlags(self, flags=0):
        """Launch a defined domain. If the call succeeds the domain moves from the
        defined to the running domains pools.
        
        If the VIR_DOMAIN_START_PAUSED flag is set, or if the guest domain
        has a managed save image that requested paused state (see
        virDomainManagedSave()) the guest domain will be started, but its
        CPUs will remain paused. The CPUs can later be manually started
        using virDomainResume().  In all other cases, the guest domain will
        be running.
        
        If the VIR_DOMAIN_START_AUTODESTROY flag is set, the guest
        domain will be automatically destroyed when the virConnectPtr
        object is finally released. This will also happen if the
        client application crashes / loses its connection to the
        libvirtd daemon. Any domains marked for auto destroy will
        block attempts at migration, save-to-file, or snapshots.
        
        If the VIR_DOMAIN_START_BYPASS_CACHE flag is set, and there is a
        managed save file for this domain (created by virDomainManagedSave()),
        then libvirt will attempt to bypass the file system cache while restoring
        the file, or fail if it cannot do so for the given system; this can allow
        less pressure on file system cache, but also risks slowing loads from NFS.
        
        If the VIR_DOMAIN_START_FORCE_BOOT flag is set, then any managed save
        file for this domain is discarded, and the domain boots from scratch. """
        ret = libvirtmod.virDomainCreateWithFlags(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainCreateWithFlags() failed', dom=self)
        return ret

    def destroy(self):
        """Destroy the domain object. The running instance is shutdown if not down
        already and all resources used by it are given back to the hypervisor. This
        does not free the associated virDomainPtr object.
        This function may require privileged access.
        
        virDomainDestroy first requests that a guest terminate
        (e.g. SIGTERM), then waits for it to comply. After a reasonable
        timeout, if the guest still exists, virDomainDestroy will
        forcefully terminate the guest (e.g. SIGKILL) if necessary (which
        may produce undesirable results, for example unflushed disk cache
        in the guest). To avoid this possibility, it's recommended to
        instead call virDomainDestroyFlags, sending the
        VIR_DOMAIN_DESTROY_GRACEFUL flag.
        
        If the domain is transient and has any snapshot metadata (see
        virDomainSnapshotNum()), then that metadata will automatically
        be deleted when the domain quits. """
        ret = libvirtmod.virDomainDestroy(self._o)
        if ret == -1: raise libvirtError ('virDomainDestroy() failed', dom=self)
        return ret

    def destroyFlags(self, flags=0):
        """Destroy the domain object. The running instance is shutdown if not down
        already and all resources used by it are given back to the hypervisor.
        This does not free the associated virDomainPtr object.
        This function may require privileged access.
        
        Calling this function with no @flags set (equal to zero) is
        equivalent to calling virDomainDestroy, and after a reasonable
        timeout will forcefully terminate the guest (e.g. SIGKILL) if
        necessary (which may produce undesirable results, for example
        unflushed disk cache in the guest). Including
        VIR_DOMAIN_DESTROY_GRACEFUL in the flags will prevent the forceful
        termination of the guest, and virDomainDestroyFlags will instead
        return an error if the guest doesn't terminate by the end of the
        timeout; at that time, the management application can decide if
        calling again without VIR_DOMAIN_DESTROY_GRACEFUL is appropriate.
        
        Another alternative which may produce cleaner results for the
        guest's disks is to use virDomainShutdown() instead, but that
        depends on guest support (some hypervisor/guest combinations may
        ignore the shutdown request). """
        ret = libvirtmod.virDomainDestroyFlags(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainDestroyFlags() failed', dom=self)
        return ret

    def detachDevice(self, xml):
        """Destroy a virtual device attachment to backend.  This function,
        having hot-unplug semantics, is only allowed on an active domain. """
        ret = libvirtmod.virDomainDetachDevice(self._o, xml)
        if ret == -1: raise libvirtError ('virDomainDetachDevice() failed', dom=self)
        return ret

    def detachDeviceFlags(self, xml, flags=0):
        """Detach a virtual device from a domain, using the flags parameter
        to control how the device is detached.  VIR_DOMAIN_AFFECT_CURRENT
        specifies that the device allocation is removed based on current domain
        state.  VIR_DOMAIN_AFFECT_LIVE specifies that the device shall be
        deallocated from the active domain instance only and is not from the
        persisted domain configuration.  VIR_DOMAIN_AFFECT_CONFIG
        specifies that the device shall be deallocated from the persisted domain
        configuration only.  Note that the target hypervisor must return an
        error if unable to satisfy flags.  E.g. the hypervisor driver will
        return failure if LIVE is specified but it only supports removing the
        persisted device allocation.
        
        Some hypervisors may prevent this operation if there is a current
        block copy operation on the device being detached; in that case,
        use virDomainBlockJobAbort() to stop the block copy first.
        
        Beware that depending on the hypervisor and device type, detaching a device
        from a running domain may be asynchronous. That is, calling
        virDomainDetachDeviceFlags may just request device removal while the device
        is actually removed later (in cooperation with a guest OS). Previously,
        this fact was ignored and the device could have been removed from domain
        configuration before it was actually removed by the hypervisor causing
        various failures on subsequent operations. To check whether the device was
        successfully removed, either recheck domain configuration using
        virDomainGetXMLDesc() or add handler for VIR_DOMAIN_EVENT_ID_DEVICE_REMOVED
        event. In case the device is already gone when virDomainDetachDeviceFlags """
        ret = libvirtmod.virDomainDetachDeviceFlags(self._o, xml, flags)
        if ret == -1: raise libvirtError ('virDomainDetachDeviceFlags() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def diskErrors(self, flags=0):
        """Extract errors on disk devices. """
        ret = libvirtmod.virDomainGetDiskErrors(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetDiskErrors() failed', dom=self)
        return ret

    def emulatorPinInfo(self, flags=0):
        """Query the CPU affinity setting of the emulator process of domain """
        ret = libvirtmod.virDomainGetEmulatorPinInfo(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetEmulatorPinInfo() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def fSTrim(self, mountPoint, minimum, flags=0):
        """Calls FITRIM within the guest (hence guest agent may be
        required depending on hypervisor used). Either call it on each
        mounted filesystem (@mountPoint is None) or just on specified
        @mountPoint. @minimum hints that free ranges smaller than this
        may be ignored (this is a hint and the guest may not respect
        it).  By increasing this value, the fstrim operation will
        complete more quickly for filesystems with badly fragmented
        free space, although not all blocks will be discarded.
        If @minimum is not zero, the command may fail. """
        ret = libvirtmod.virDomainFSTrim(self._o, mountPoint, minimum, flags)
        if ret == -1: raise libvirtError ('virDomainFSTrim() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def getCPUStats(self, total, flags=0):
        """Extracts CPU statistics for a running domain. On success it will
           return a list of data of dictionary type. If boolean total is False or 0, the
           first element of the list refers to CPU0 on the host, second element is
           CPU1, and so on. The format of data struct is as follows:
           [{cpu_time:xxx}, {cpu_time:xxx}, ...]
           If it is True or 1, it returns total domain CPU statistics in the format of
           [{cpu_time:xxx, user_time:xxx, system_time:xxx}] """
        ret = libvirtmod.virDomainGetCPUStats(self._o, total, flags)
        if ret is None: raise libvirtError ('virDomainGetCPUStats() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def hasCurrentSnapshot(self, flags=0):
        """Determine if the domain has a current snapshot. """
        ret = libvirtmod.virDomainHasCurrentSnapshot(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainHasCurrentSnapshot() failed', dom=self)
        return ret

    def hasManagedSaveImage(self, flags=0):
        """Check if a domain has a managed save image as created by
        virDomainManagedSave(). Note that any running domain should not have
        such an image, as it should have been removed on restart. """
        ret = libvirtmod.virDomainHasManagedSaveImage(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainHasManagedSaveImage() failed', dom=self)
        return ret

    def hostname(self, flags=0):
        """Get the hostname for that domain.
        
        Dependent on hypervisor used, this may require a guest agent to be
        available. """
        ret = libvirtmod.virDomainGetHostname(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetHostname() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def info(self):
        """Extract information about a domain. Note that if the connection used to get the domain is limited only a partial set of the information can be extracted. """
        ret = libvirtmod.virDomainGetInfo(self._o)
        if ret is None: raise libvirtError ('virDomainGetInfo() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def injectNMI(self, flags=0):
        """Send NMI to the guest """
        ret = libvirtmod.virDomainInjectNMI(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainInjectNMI() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def interfaceParameters(self, device, flags=0):
        """Get the bandwidth tunables for a interface device """
        ret = libvirtmod.virDomainGetInterfaceParameters(self._o, device, flags)
        if ret is None: raise libvirtError ('virDomainGetInterfaceParameters() failed', dom=self)
        return ret

    def interfaceStats(self, path):
        """Extracts interface device statistics for a domain """
        ret = libvirtmod.virDomainInterfaceStats(self._o, path)
        if ret is None: raise libvirtError ('virDomainInterfaceStats() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def isActive(self):
        """Determine if the domain is currently running """
        ret = libvirtmod.virDomainIsActive(self._o)
        if ret == -1: raise libvirtError ('virDomainIsActive() failed', dom=self)
        return ret

    def isPersistent(self):
        """Determine if the domain has a persistent configuration
        which means it will still exist after shutting down """
        ret = libvirtmod.virDomainIsPersistent(self._o)
        if ret == -1: raise libvirtError ('virDomainIsPersistent() failed', dom=self)
        return ret

    def isUpdated(self):
        """Determine if the domain has been updated. """
        ret = libvirtmod.virDomainIsUpdated(self._o)
        if ret == -1: raise libvirtError ('virDomainIsUpdated() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def jobInfo(self):
        """Extract information about an active job being processed for a domain. """
        ret = libvirtmod.virDomainGetJobInfo(self._o)
        if ret is None: raise libvirtError ('virDomainGetJobInfo() failed', dom=self)
        return ret

    def jobStats(self, flags=0):
        """Extract information about an active job being processed for a domain. """
        ret = libvirtmod.virDomainGetJobStats(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetJobStats() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def managedSave(self, flags=0):
        """This method will suspend a domain and save its memory contents to
        a file on disk. After the call, if successful, the domain is not
        listed as running anymore.
        The difference from virDomainSave() is that libvirt is keeping track of
        the saved state itself, and will reuse it once the domain is being
        restarted (automatically or via an explicit libvirt call).
        As a result any running domain is sure to not have a managed saved image.
        This also implies that managed save only works on persistent domains,
        since the domain must still exist in order to use virDomainCreate() to
        restart it.
        
        If @flags includes VIR_DOMAIN_SAVE_BYPASS_CACHE, then libvirt will
        attempt to bypass the file system cache while creating the file, or
        fail if it cannot do so for the given system; this can allow less
        pressure on file system cache, but also risks slowing saves to NFS.
        
        Normally, the managed saved state will remember whether the domain
        was running or paused, and start will resume to the same state.
        Specifying VIR_DOMAIN_SAVE_RUNNING or VIR_DOMAIN_SAVE_PAUSED in
        @flags will override the default saved into the file.  These two
        flags are mutually exclusive. """
        ret = libvirtmod.virDomainManagedSave(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainManagedSave() failed', dom=self)
        return ret

    def managedSaveRemove(self, flags=0):
        """Remove any managed save image for this domain. """
        ret = libvirtmod.virDomainManagedSaveRemove(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainManagedSaveRemove() failed', dom=self)
        return ret

    def maxMemory(self):
        """Retrieve the maximum amount of physical memory allocated to a
        domain. If domain is None, then this get the amount of memory reserved
        to Domain0 i.e. the domain where the application runs. """
        ret = libvirtmod.virDomainGetMaxMemory(self._o)
        if ret == 0: raise libvirtError ('virDomainGetMaxMemory() failed', dom=self)
        return ret

    def maxVcpus(self):
        """Provides the maximum number of virtual CPUs supported for
        the guest VM. If the guest is inactive, this is basically
        the same as virConnectGetMaxVcpus(). If the guest is running
        this will reflect the maximum number of virtual CPUs the
        guest was booted with.  For more details, see virDomainGetVcpusFlags(). """
        ret = libvirtmod.virDomainGetMaxVcpus(self._o)
        if ret == -1: raise libvirtError ('virDomainGetMaxVcpus() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def memoryParameters(self, flags=0):
        """Get the memory parameters """
        ret = libvirtmod.virDomainGetMemoryParameters(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetMemoryParameters() failed', dom=self)
        return ret

    def memoryPeek(self, start, size, flags=0):
        """Read the contents of domain's memory """
        ret = libvirtmod.virDomainMemoryPeek(self._o, start, size, flags)
        if ret is None: raise libvirtError ('virDomainMemoryPeek() failed', dom=self)
        return ret

    def memoryStats(self):
        """Extracts memory statistics for a domain """
        ret = libvirtmod.virDomainMemoryStats(self._o)
        if ret is None: raise libvirtError ('virDomainMemoryStats() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def metadata(self, type, uri, flags=0):
        """Retrieves the appropriate domain element given by @type.
        If VIR_DOMAIN_METADATA_ELEMENT is requested parameter @uri
        must be set to the name of the namespace the requested elements
        belong to, otherwise must be None.
        
        If an element of the domain XML is not present, the resulting
        error will be VIR_ERR_NO_DOMAIN_METADATA.  This method forms
        a shortcut for seeing information from virDomainSetMetadata()
        without having to go through virDomainGetXMLDesc().
        
        @flags controls whether the live domain or persistent
        configuration will be queried. """
        ret = libvirtmod.virDomainGetMetadata(self._o, type, uri, flags)
        if ret is None: raise libvirtError ('virDomainGetMetadata() failed', dom=self)
        return ret

    def migrate(self, dconn, flags=0, dname=None, uri=None, bandwidth=0):
        """Migrate the domain object from its current host to the destination
        host given by dconn (a connection to the destination host).
        
        Flags may be one of more of the following:
          VIR_MIGRATE_LIVE      Do not pause the VM during migration
          VIR_MIGRATE_PEER2PEER Direct connection between source & destination hosts
          VIR_MIGRATE_TUNNELLED Tunnel migration data over the libvirt RPC channel
          VIR_MIGRATE_PERSIST_DEST If the migration is successful, persist the domain
                                   on the destination host.
          VIR_MIGRATE_UNDEFINE_SOURCE If the migration is successful, undefine the
                                      domain on the source host.
          VIR_MIGRATE_PAUSED    Leave the domain suspended on the remote side.
          VIR_MIGRATE_NON_SHARED_DISK Migration with non-shared storage with full
                                      disk copy
          VIR_MIGRATE_NON_SHARED_INC  Migration with non-shared storage with
                                      incremental disk copy
          VIR_MIGRATE_CHANGE_PROTECTION Protect against domain configuration
                                        changes during the migration process (set
                                        automatically when supported).
          VIR_MIGRATE_UNSAFE    Force migration even if it is considered unsafe.
          VIR_MIGRATE_OFFLINE Migrate offline
        
        VIR_MIGRATE_TUNNELLED requires that VIR_MIGRATE_PEER2PEER be set.
        Applications using the VIR_MIGRATE_PEER2PEER flag will probably
        prefer to invoke virDomainMigrateToURI, avoiding the need to
        open connection to the destination host themselves.
        
        If a hypervisor supports renaming domains during migration,
        then you may set the dname parameter to the new name (otherwise
        it keeps the same name).  If this is not supported by the
        hypervisor, dname must be None or else you will get an error.
        
        If the VIR_MIGRATE_PEER2PEER flag is set, the uri parameter
        must be a valid libvirt connection URI, by which the source
        libvirt driver can connect to the destination libvirt. If
        omitted, the dconn connection object will be queried for its
        current URI.
        
        If the VIR_MIGRATE_PEER2PEER flag is NOT set, the URI parameter
        takes a hypervisor specific format. The hypervisor capabilities
        XML includes details of the support URI schemes. If omitted
        the dconn will be asked for a default URI.
        
        If you want to copy non-shared storage within migration you
        can use either VIR_MIGRATE_NON_SHARED_DISK or
        VIR_MIGRATE_NON_SHARED_INC as they are mutually exclusive.
        
        In either case it is typically only necessary to specify a
        URI if the destination host has multiple interfaces and a
        specific interface is required to transmit migration data.
        
        The maximum bandwidth (in MiB/s) that will be used to do migration
        can be specified with the bandwidth parameter.  If set to 0,
        libvirt will choose a suitable default.  Some hypervisors do
        not support this feature and will return an error if bandwidth
        is not 0.
        
        To see which features are supported by the current hypervisor,
        see virConnectGetCapabilities, /capabilities/host/migration_features.
        
        There are many limitations on migration imposed by the underlying
        technology - for example it may not be possible to migrate between
        different processors even with the same architecture, or between
        different types of hypervisor. """
        if dconn is None: dconn__o = None
        else: dconn__o = dconn._o
        ret = libvirtmod.virDomainMigrate(self._o, dconn__o, flags, dname, uri, bandwidth)
        if ret is None:raise libvirtError('virDomainMigrate() failed', dom=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    def migrate2(self, dconn, dxml=None, flags=0, dname=None, uri=None, bandwidth=0):
        """Migrate the domain object from its current host to the destination
        host given by dconn (a connection to the destination host).
        
        Flags may be one of more of the following:
          VIR_MIGRATE_LIVE      Do not pause the VM during migration
          VIR_MIGRATE_PEER2PEER Direct connection between source & destination hosts
          VIR_MIGRATE_TUNNELLED Tunnel migration data over the libvirt RPC channel
          VIR_MIGRATE_PERSIST_DEST If the migration is successful, persist the domain
                                   on the destination host.
          VIR_MIGRATE_UNDEFINE_SOURCE If the migration is successful, undefine the
                                      domain on the source host.
          VIR_MIGRATE_PAUSED    Leave the domain suspended on the remote side.
          VIR_MIGRATE_NON_SHARED_DISK Migration with non-shared storage with full
                                      disk copy
          VIR_MIGRATE_NON_SHARED_INC  Migration with non-shared storage with
                                      incremental disk copy
          VIR_MIGRATE_CHANGE_PROTECTION Protect against domain configuration
                                        changes during the migration process (set
                                        automatically when supported).
          VIR_MIGRATE_UNSAFE    Force migration even if it is considered unsafe.
          VIR_MIGRATE_OFFLINE Migrate offline
        
        VIR_MIGRATE_TUNNELLED requires that VIR_MIGRATE_PEER2PEER be set.
        Applications using the VIR_MIGRATE_PEER2PEER flag will probably
        prefer to invoke virDomainMigrateToURI, avoiding the need to
        open connection to the destination host themselves.
        
        If a hypervisor supports renaming domains during migration,
        then you may set the dname parameter to the new name (otherwise
        it keeps the same name).  If this is not supported by the
        hypervisor, dname must be None or else you will get an error.
        
        If the VIR_MIGRATE_PEER2PEER flag is set, the uri parameter
        must be a valid libvirt connection URI, by which the source
        libvirt driver can connect to the destination libvirt. If
        omitted, the dconn connection object will be queried for its
        current URI.
        
        If the VIR_MIGRATE_PEER2PEER flag is NOT set, the URI parameter
        takes a hypervisor specific format. The hypervisor capabilities
        XML includes details of the support URI schemes. If omitted
        the dconn will be asked for a default URI.
        
        If you want to copy non-shared storage within migration you
        can use either VIR_MIGRATE_NON_SHARED_DISK or
        VIR_MIGRATE_NON_SHARED_INC as they are mutually exclusive.
        
        In either case it is typically only necessary to specify a
        URI if the destination host has multiple interfaces and a
        specific interface is required to transmit migration data.
        
        The maximum bandwidth (in MiB/s) that will be used to do migration
        can be specified with the bandwidth parameter.  If set to 0,
        libvirt will choose a suitable default.  Some hypervisors do
        not support this feature and will return an error if bandwidth
        is not 0.
        
        To see which features are supported by the current hypervisor,
        see virConnectGetCapabilities, /capabilities/host/migration_features.
        
        There are many limitations on migration imposed by the underlying
        technology - for example it may not be possible to migrate between
        different processors even with the same architecture, or between
        different types of hypervisor.
        
        If the hypervisor supports it, @dxml can be used to alter
        host-specific portions of the domain XML that will be used on
        the destination.  For example, it is possible to alter the
        backing filename that is associated with a disk device, in order
        to account for naming differences between source and destination
        in accessing the underlying storage.  The migration will fail
        if @dxml would cause any guest-visible changes.  Pass None
        if no changes are needed to the XML between source and destination.
        @dxml cannot be used to rename the domain during migration (use
        @dname for that purpose).  Domain name in @dxml must match the
        original domain name. """
        if dconn is None: dconn__o = None
        else: dconn__o = dconn._o
        ret = libvirtmod.virDomainMigrate2(self._o, dconn__o, dxml, flags, dname, uri, bandwidth)
        if ret is None:raise libvirtError('virDomainMigrate2() failed', dom=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    #
    # virDomain functions from module python
    #

    def migrate3(self, dconn, params, flags=0):
        """Migrate the domain object from its current host to the destination host
                    given by dconn (a connection to the destination host). """
        if dconn is None: dconn__o = None
        else: dconn__o = dconn._o
        ret = libvirtmod.virDomainMigrate3(self._o, dconn__o, params, flags)
        if ret is None:raise libvirtError('virDomainMigrate3() failed', dom=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    def migrateGetCompressionCache(self, flags=0):
        """Get current size of the cache (in bytes) used for compressing
                    repeatedly transferred memory pages during live migration. """
        ret = libvirtmod.virDomainMigrateGetCompressionCache(self._o, flags)
        return ret

    def migrateGetMaxSpeed(self, flags=0):
        """Get currently configured maximum migration speed for a domain """
        ret = libvirtmod.virDomainMigrateGetMaxSpeed(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainMigrateGetMaxSpeed() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def migrateSetCompressionCache(self, cacheSize, flags=0):
        """Sets size of the cache (in bytes) used for compressing repeatedly
        transferred memory pages during live migration. It's supposed to be called
        while the domain is being live-migrated as a reaction to migration progress
        and increasing number of compression cache misses obtained from
        virDomainGetJobStats. """
        ret = libvirtmod.virDomainMigrateSetCompressionCache(self._o, cacheSize, flags)
        if ret == -1: raise libvirtError ('virDomainMigrateSetCompressionCache() failed', dom=self)
        return ret

    def migrateSetMaxDowntime(self, downtime, flags=0):
        """Sets maximum tolerable time for which the domain is allowed to be paused
        at the end of live migration. It's supposed to be called while the domain is
        being live-migrated as a reaction to migration progress. """
        ret = libvirtmod.virDomainMigrateSetMaxDowntime(self._o, downtime, flags)
        if ret == -1: raise libvirtError ('virDomainMigrateSetMaxDowntime() failed', dom=self)
        return ret

    def migrateSetMaxSpeed(self, bandwidth, flags=0):
        """The maximum bandwidth (in MiB/s) that will be used to do migration
        can be specified with the bandwidth parameter. Not all hypervisors
        will support a bandwidth cap """
        ret = libvirtmod.virDomainMigrateSetMaxSpeed(self._o, bandwidth, flags)
        if ret == -1: raise libvirtError ('virDomainMigrateSetMaxSpeed() failed', dom=self)
        return ret

    def migrateToURI(self, duri, flags=0, dname=None, bandwidth=0):
        """Migrate the domain object from its current host to the destination
        host given by duri.
        
        Flags may be one of more of the following:
          VIR_MIGRATE_LIVE      Do not pause the VM during migration
          VIR_MIGRATE_PEER2PEER Direct connection between source & destination hosts
          VIR_MIGRATE_TUNNELLED Tunnel migration data over the libvirt RPC channel
          VIR_MIGRATE_PERSIST_DEST If the migration is successful, persist the domain
                                   on the destination host.
          VIR_MIGRATE_UNDEFINE_SOURCE If the migration is successful, undefine the
                                      domain on the source host.
          VIR_MIGRATE_PAUSED    Leave the domain suspended on the remote side.
          VIR_MIGRATE_NON_SHARED_DISK Migration with non-shared storage with full
                                      disk copy
          VIR_MIGRATE_NON_SHARED_INC  Migration with non-shared storage with
                                      incremental disk copy
          VIR_MIGRATE_CHANGE_PROTECTION Protect against domain configuration
                                        changes during the migration process (set
                                        automatically when supported).
          VIR_MIGRATE_UNSAFE    Force migration even if it is considered unsafe.
          VIR_MIGRATE_OFFLINE Migrate offline
        
        The operation of this API hinges on the VIR_MIGRATE_PEER2PEER flag.
        If the VIR_MIGRATE_PEER2PEER flag is NOT set, the duri parameter
        takes a hypervisor specific format. The uri_transports element of the
        hypervisor capabilities XML includes details of the supported URI
        schemes. Not all hypervisors will support this mode of migration, so
        if the VIR_MIGRATE_PEER2PEER flag is not set, then it may be necessary
        to use the alternative virDomainMigrate API providing and explicit
        virConnectPtr for the destination host.
        
        If the VIR_MIGRATE_PEER2PEER flag IS set, the duri parameter
        must be a valid libvirt connection URI, by which the source
        libvirt driver can connect to the destination libvirt.
        
        VIR_MIGRATE_TUNNELLED requires that VIR_MIGRATE_PEER2PEER be set.
        
        If you want to copy non-shared storage within migration you
        can use either VIR_MIGRATE_NON_SHARED_DISK or
        VIR_MIGRATE_NON_SHARED_INC as they are mutually exclusive.
        
        If a hypervisor supports renaming domains during migration,
        the dname parameter specifies the new name for the domain.
        Setting dname to None keeps the domain name the same.  If domain
        renaming is not supported by the hypervisor, dname must be None or
        else an error will be returned.
        
        The maximum bandwidth (in MiB/s) that will be used to do migration
        can be specified with the bandwidth parameter.  If set to 0,
        libvirt will choose a suitable default.  Some hypervisors do
        not support this feature and will return an error if bandwidth
        is not 0.
        
        To see which features are supported by the current hypervisor,
        see virConnectGetCapabilities, /capabilities/host/migration_features.
        
        There are many limitations on migration imposed by the underlying
        technology - for example it may not be possible to migrate between
        different processors even with the same architecture, or between
        different types of hypervisor. """
        ret = libvirtmod.virDomainMigrateToURI(self._o, duri, flags, dname, bandwidth)
        if ret == -1: raise libvirtError ('virDomainMigrateToURI() failed', dom=self)
        return ret

    def migrateToURI2(self, dconnuri=None, miguri=None, dxml=None, flags=0, dname=None, bandwidth=0):
        """Migrate the domain object from its current host to the destination
        host given by duri.
        
        Flags may be one of more of the following:
          VIR_MIGRATE_LIVE      Do not pause the VM during migration
          VIR_MIGRATE_PEER2PEER Direct connection between source & destination hosts
          VIR_MIGRATE_TUNNELLED Tunnel migration data over the libvirt RPC channel
          VIR_MIGRATE_PERSIST_DEST If the migration is successful, persist the domain
                                   on the destination host.
          VIR_MIGRATE_UNDEFINE_SOURCE If the migration is successful, undefine the
                                      domain on the source host.
          VIR_MIGRATE_PAUSED    Leave the domain suspended on the remote side.
          VIR_MIGRATE_NON_SHARED_DISK Migration with non-shared storage with full
                                      disk copy
          VIR_MIGRATE_NON_SHARED_INC  Migration with non-shared storage with
                                      incremental disk copy
          VIR_MIGRATE_CHANGE_PROTECTION Protect against domain configuration
                                        changes during the migration process (set
                                        automatically when supported).
          VIR_MIGRATE_UNSAFE    Force migration even if it is considered unsafe.
          VIR_MIGRATE_OFFLINE Migrate offline
        
        The operation of this API hinges on the VIR_MIGRATE_PEER2PEER flag.
        
        If the VIR_MIGRATE_PEER2PEER flag is set, the @dconnuri parameter
        must be a valid libvirt connection URI, by which the source
        libvirt driver can connect to the destination libvirt. If the
        VIR_MIGRATE_PEER2PEER flag is NOT set, then @dconnuri must be
        None.
        
        If the VIR_MIGRATE_TUNNELLED flag is NOT set, then the @miguri
        parameter allows specification of a URI to use to initiate the
        VM migration. It takes a hypervisor specific format. The uri_transports
        element of the hypervisor capabilities XML includes details of the
        supported URI schemes.
        
        VIR_MIGRATE_TUNNELLED requires that VIR_MIGRATE_PEER2PEER be set.
        
        If you want to copy non-shared storage within migration you
        can use either VIR_MIGRATE_NON_SHARED_DISK or
        VIR_MIGRATE_NON_SHARED_INC as they are mutually exclusive.
        
        If a hypervisor supports changing the configuration of the guest
        during migration, the @dxml parameter specifies the new config
        for the guest. The configuration must include an identical set
        of virtual devices, to ensure a stable guest ABI across migration.
        Only parameters related to host side configuration can be
        changed in the XML. Hypervisors will validate this and refuse to
        allow migration if the provided XML would cause a change in the
        guest ABI,
        
        If a hypervisor supports renaming domains during migration,
        the dname parameter specifies the new name for the domain.
        Setting dname to None keeps the domain name the same.  If domain
        renaming is not supported by the hypervisor, dname must be None or
        else an error will be returned.
        
        The maximum bandwidth (in MiB/s) that will be used to do migration
        can be specified with the bandwidth parameter.  If set to 0,
        libvirt will choose a suitable default.  Some hypervisors do
        not support this feature and will return an error if bandwidth
        is not 0.
        
        To see which features are supported by the current hypervisor,
        see virConnectGetCapabilities, /capabilities/host/migration_features.
        
        There are many limitations on migration imposed by the underlying
        technology - for example it may not be possible to migrate between
        different processors even with the same architecture, or between
        different types of hypervisor. """
        ret = libvirtmod.virDomainMigrateToURI2(self._o, dconnuri, miguri, dxml, flags, dname, bandwidth)
        if ret == -1: raise libvirtError ('virDomainMigrateToURI2() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def migrateToURI3(self, dconnuri, params, flags=0):
        """Migrate the domain object from its current host to the destination host
                    given by URI. """
        if dconnuri is None: dconnuri__o = None
        else: dconnuri__o = dconnuri._o
        ret = libvirtmod.virDomainMigrateToURI3(self._o, dconnuri__o, params, flags)
        if ret == -1: raise libvirtError ('virDomainMigrateToURI3() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def name(self):
        """Get the public name for that domain """
        ret = libvirtmod.virDomainGetName(self._o)
        return ret

    #
    # virDomain functions from module python
    #

    def numaParameters(self, flags=0):
        """Get the NUMA parameters """
        ret = libvirtmod.virDomainGetNumaParameters(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetNumaParameters() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def openChannel(self, name, st, flags=0):
        """This opens the host interface associated with a channel device on a
        guest, if the host interface is supported.  If @name is given, it
        can match either the device alias (e.g. "channel0"), or the virtio
        target name (e.g. "org.qemu.guest_agent.0").  If @name is omitted,
        then the first channel is opened. The channel is associated with
        the passed in @st stream, which should have been opened in
        non-blocking mode for bi-directional I/O.
        
        By default, when @flags is 0, the open will fail if libvirt detects
        that the channel is already in use by another client; passing
        VIR_DOMAIN_CHANNEL_FORCE will cause libvirt to forcefully remove the
        other client prior to opening this channel. """
        if st is None: st__o = None
        else: st__o = st._o
        ret = libvirtmod.virDomainOpenChannel(self._o, name, st__o, flags)
        if ret == -1: raise libvirtError ('virDomainOpenChannel() failed', dom=self)
        return ret

    def openConsole(self, dev_name, st, flags=0):
        """This opens the backend associated with a console, serial or
        parallel port device on a guest, if the backend is supported.
        If the @dev_name is omitted, then the first console or serial
        device is opened. The console is associated with the passed
        in @st stream, which should have been opened in non-blocking
        mode for bi-directional I/O.
        
        By default, when @flags is 0, the open will fail if libvirt
        detects that the console is already in use by another client;
        passing VIR_DOMAIN_CONSOLE_FORCE will cause libvirt to forcefully
        remove the other client prior to opening this console.
        
        If flag VIR_DOMAIN_CONSOLE_SAFE the console is opened only in the
        case where the hypervisor driver supports safe (mutually exclusive)
        console handling.
        
        Older servers did not support either flag, and also did not forbid
        simultaneous clients on a console, with potentially confusing results.
        When passing @flags of 0 in order to support a wider range of server
        versions, it is up to the client to ensure mutual exclusion. """
        if st is None: st__o = None
        else: st__o = st._o
        ret = libvirtmod.virDomainOpenConsole(self._o, dev_name, st__o, flags)
        if ret == -1: raise libvirtError ('virDomainOpenConsole() failed', dom=self)
        return ret

    def openGraphics(self, idx, fd, flags=0):
        """This will attempt to connect the file descriptor @fd, to
        the graphics backend of @dom. If @dom has multiple graphics
        backends configured, then @idx will determine which one is
        opened, starting from @idx 0.
        
        To disable any authentication, pass the VIR_DOMAIN_OPEN_GRAPHICS_SKIPAUTH
        constant for @flags.
        
        The caller should use an anonymous socketpair to open
        @fd before invocation.
        
        This method can only be used when connected to a local
        libvirt hypervisor, over a UNIX domain socket. Attempts
        to use this method over a TCP connection will always fail """
        ret = libvirtmod.virDomainOpenGraphics(self._o, idx, fd, flags)
        if ret == -1: raise libvirtError ('virDomainOpenGraphics() failed', dom=self)
        return ret

    def pMSuspendForDuration(self, target, duration, flags=0):
        """Attempt to have the guest enter the given @target power management
        suspension level.  If @duration is non-zero, also schedule the guest to
        resume normal operation after that many seconds, if nothing else has
        resumed it earlier.  Some hypervisors require that @duration be 0, for
        an indefinite suspension.
        
        Dependent on hypervisor used, this may require a
        guest agent to be available, e.g. QEMU.
        
        Beware that at least for QEMU, the domain's process will be terminated
        when VIR_NODE_SUSPEND_TARGET_DISK is used and a new process will be
        launched when libvirt is asked to wake up the domain. As a result of
        this, any runtime changes, such as device hotplug or memory settings,
        are lost unless such changes were made with VIR_DOMAIN_AFFECT_CONFIG
        flag. """
        ret = libvirtmod.virDomainPMSuspendForDuration(self._o, target, duration, flags)
        if ret == -1: raise libvirtError ('virDomainPMSuspendForDuration() failed', dom=self)
        return ret

    def pMWakeup(self, flags=0):
        """Inject a wakeup into the guest that previously used
        virDomainPMSuspendForDuration, rather than waiting for the
        previously requested duration (if any) to elapse. """
        ret = libvirtmod.virDomainPMWakeup(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainPMWakeup() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def pinEmulator(self, cpumap, flags=0):
        """Dynamically change the real CPUs which can be allocated to the emulator process of a domain.
                    This function requires privileged access to the hypervisor. """
        ret = libvirtmod.virDomainPinEmulator(self._o, cpumap, flags)
        if ret == -1: raise libvirtError ('virDomainPinEmulator() failed', dom=self)
        return ret

    def pinVcpu(self, vcpu, cpumap):
        """Dynamically change the real CPUs which can be allocated to a virtual CPU. This function requires privileged access to the hypervisor. """
        ret = libvirtmod.virDomainPinVcpu(self._o, vcpu, cpumap)
        if ret == -1: raise libvirtError ('virDomainPinVcpu() failed', dom=self)
        return ret

    def pinVcpuFlags(self, vcpu, cpumap, flags=0):
        """Dynamically change the real CPUs which can be allocated to a virtual CPU. This function requires privileged access to the hypervisor. """
        ret = libvirtmod.virDomainPinVcpuFlags(self._o, vcpu, cpumap, flags)
        if ret == -1: raise libvirtError ('virDomainPinVcpuFlags() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def reboot(self, flags=0):
        """Reboot a domain, the domain object is still usable thereafter, but
        the domain OS is being stopped for a restart.
        Note that the guest OS may ignore the request.
        Additionally, the hypervisor may check and support the domain
        'on_reboot' XML setting resulting in a domain that shuts down instead
        of rebooting.
        
        If @flags is set to zero, then the hypervisor will choose the
        method of shutdown it considers best. To have greater control
        pass one or more of the virDomainShutdownFlagValues. The order
        in which the hypervisor tries each shutdown method is undefined,
        and a hypervisor is not required to support all methods.
        
        To use guest agent (VIR_DOMAIN_REBOOT_GUEST_AGENT) the domain XML
        must have <channel> configured.
        
        Due to implementation limitations in some drivers (the qemu driver,
        for instance) it is not advised to migrate or save a guest that is
        rebooting as a result of this API. Migrating such a guest can lead
        to a plain shutdown on the destination. """
        ret = libvirtmod.virDomainReboot(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainReboot() failed', dom=self)
        return ret

    def reset(self, flags=0):
        """Reset a domain immediately without any guest OS shutdown.
        Reset emulates the power reset button on a machine, where all
        hardware sees the RST line set and reinitializes internal state.
        
        Note that there is a risk of data loss caused by reset without any
        guest OS shutdown. """
        ret = libvirtmod.virDomainReset(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainReset() failed', dom=self)
        return ret

    def resume(self):
        """Resume a suspended domain, the process is restarted from the state where
        it was frozen by calling virDomainSuspend().
        This function may require privileged access
        Moreover, resume may not be supported if domain is in some
        special state like VIR_DOMAIN_PMSUSPENDED. """
        ret = libvirtmod.virDomainResume(self._o)
        if ret == -1: raise libvirtError ('virDomainResume() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def revertToSnapshot(self, snap, flags=0):
        """revert the domain to the given snapshot """
        if snap is None: snap__o = None
        else: snap__o = snap._o
        ret = libvirtmod.virDomainRevertToSnapshot(self._o, snap__o, flags)
        if ret == -1: raise libvirtError ('virDomainRevertToSnapshot() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def save(self, to):
        """This method will suspend a domain and save its memory contents to
        a file on disk. After the call, if successful, the domain is not
        listed as running anymore (this ends the life of a transient domain).
        Use virDomainRestore() to restore a domain after saving.
        
        See virDomainSaveFlags() for more control.  Also, a save file can
        be inspected or modified slightly with virDomainSaveImageGetXMLDesc()
        and virDomainSaveImageDefineXML(). """
        ret = libvirtmod.virDomainSave(self._o, to)
        if ret == -1: raise libvirtError ('virDomainSave() failed', dom=self)
        return ret

    def saveFlags(self, to, dxml=None, flags=0):
        """This method will suspend a domain and save its memory contents to
        a file on disk. After the call, if successful, the domain is not
        listed as running anymore (this ends the life of a transient domain).
        Use virDomainRestore() to restore a domain after saving.
        
        If the hypervisor supports it, @dxml can be used to alter
        host-specific portions of the domain XML that will be used when
        restoring an image.  For example, it is possible to alter the
        backing filename that is associated with a disk device, in order to
        prepare for file renaming done as part of backing up the disk
        device while the domain is stopped.
        
        If @flags includes VIR_DOMAIN_SAVE_BYPASS_CACHE, then libvirt will
        attempt to bypass the file system cache while creating the file, or
        fail if it cannot do so for the given system; this can allow less
        pressure on file system cache, but also risks slowing saves to NFS.
        
        Normally, the saved state file will remember whether the domain was
        running or paused, and restore defaults to the same state.
        Specifying VIR_DOMAIN_SAVE_RUNNING or VIR_DOMAIN_SAVE_PAUSED in
        @flags will override what state gets saved into the file.  These
        two flags are mutually exclusive.
        
        A save file can be inspected or modified slightly with
        virDomainSaveImageGetXMLDesc() and virDomainSaveImageDefineXML().
        
        Some hypervisors may prevent this operation if there is a current
        block copy operation; in that case, use virDomainBlockJobAbort()
        to stop the block copy first. """
        ret = libvirtmod.virDomainSaveFlags(self._o, to, dxml, flags)
        if ret == -1: raise libvirtError ('virDomainSaveFlags() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def schedulerParameters(self):
        """Get the scheduler parameters, the @params array will be filled with the values. """
        ret = libvirtmod.virDomainGetSchedulerParameters(self._o)
        if ret is None: raise libvirtError ('virDomainGetSchedulerParameters() failed', dom=self)
        return ret

    def schedulerParametersFlags(self, flags=0):
        """Get the scheduler parameters """
        ret = libvirtmod.virDomainGetSchedulerParametersFlags(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetSchedulerParametersFlags() failed', dom=self)
        return ret

    def schedulerType(self):
        """Get the scheduler type. """
        ret = libvirtmod.virDomainGetSchedulerType(self._o)
        if ret is None: raise libvirtError ('virDomainGetSchedulerType() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def screenshot(self, stream, screen, flags=0):
        """Take a screenshot of current domain console as a stream. The image format
        is hypervisor specific. Moreover, some hypervisors supports multiple
        displays per domain. These can be distinguished by @screen argument.
        
        This call sets up a stream; subsequent use of stream API is necessary
        to transfer actual data, determine how much data is successfully
        transferred, and detect any errors.
        
        The screen ID is the sequential number of screen. In case of multiple
        graphics cards, heads are enumerated before devices, e.g. having
        two graphics cards, both with four heads, screen ID 5 addresses
        the second head on the second card. """
        if stream is None: stream__o = None
        else: stream__o = stream._o
        ret = libvirtmod.virDomainScreenshot(self._o, stream__o, screen, flags)
        if ret is None: raise libvirtError ('virDomainScreenshot() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def securityLabel(self):
        """Extract information about the domain security label. Only the first label will be returned. """
        ret = libvirtmod.virDomainGetSecurityLabel(self._o)
        if ret is None: raise libvirtError ('virDomainGetSecurityLabel() failed', dom=self)
        return ret

    def securityLabelList(self):
        """Extract information about the domain security label. A list of all labels will be returned. """
        ret = libvirtmod.virDomainGetSecurityLabelList(self._o)
        if ret is None: raise libvirtError ('virDomainGetSecurityLabelList() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def sendKey(self, codeset, holdtime, keycodes, nkeycodes, flags=0):
        """Send key(s) to the guest. """
        ret = libvirtmod.virDomainSendKey(self._o, codeset, holdtime, keycodes, nkeycodes, flags)
        if ret == -1: raise libvirtError ('virDomainSendKey() failed', dom=self)
        return ret

    def sendProcessSignal(self, pid_value, signum, flags=0):
        """Send a signal to the designated process in the guest
        
        The signal numbers must be taken from the virDomainProcessSignal
        enum. These will be translated to the corresponding signal
        number for the guest OS, by the guest agent delivering the
        signal. If there is no mapping from virDomainProcessSignal to
        the native OS signals, this API will report an error.
        
        If @pid_value is an integer greater than zero, it is
        treated as a process ID. If @pid_value is an integer
        less than zero, it is treated as a process group ID.
        All the @pid_value numbers are from the container/guest
        namespace. The value zero is not valid.
        
        Not all hypervisors will support sending signals to
        arbitrary processes or process groups. If this API is
        implemented the minimum requirement is to be able to
        use @pid_value==1 (i.e. kill init). No other value is
        required to be supported.
        
        If the @signum is VIR_DOMAIN_PROCESS_SIGNAL_NOP then this
        API will simply report whether the process is running in
        the container/guest. """
        ret = libvirtmod.virDomainSendProcessSignal(self._o, pid_value, signum, flags)
        if ret == -1: raise libvirtError ('virDomainSendProcessSignal() failed', dom=self)
        return ret

    def setAutostart(self, autostart):
        """Configure the domain to be automatically started
        when the host machine boots. """
        ret = libvirtmod.virDomainSetAutostart(self._o, autostart)
        if ret == -1: raise libvirtError ('virDomainSetAutostart() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def setBlkioParameters(self, params, flags=0):
        """Change the blkio tunables """
        ret = libvirtmod.virDomainSetBlkioParameters(self._o, params, flags)
        if ret == -1: raise libvirtError ('virDomainSetBlkioParameters() failed', dom=self)
        return ret

    def setBlockIoTune(self, disk, params, flags=0):
        """Change the I/O tunables for a block device """
        ret = libvirtmod.virDomainSetBlockIoTune(self._o, disk, params, flags)
        if ret == -1: raise libvirtError ('virDomainSetBlockIoTune() failed', dom=self)
        return ret

    def setInterfaceParameters(self, device, params, flags=0):
        """Change the bandwidth tunables for a interface device """
        ret = libvirtmod.virDomainSetInterfaceParameters(self._o, device, params, flags)
        if ret == -1: raise libvirtError ('virDomainSetInterfaceParameters() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def setMaxMemory(self, memory):
        """Dynamically change the maximum amount of physical memory allocated to a
        domain. If domain is None, then this change the amount of memory reserved
        to Domain0 i.e. the domain where the application runs.
        This function may require privileged access to the hypervisor.
        
        This command is hypervisor-specific for whether active, persistent,
        or both configurations are changed; for more control, use
        virDomainSetMemoryFlags(). """
        ret = libvirtmod.virDomainSetMaxMemory(self._o, memory)
        if ret == -1: raise libvirtError ('virDomainSetMaxMemory() failed', dom=self)
        return ret

    def setMemory(self, memory):
        """Dynamically change the target amount of physical memory allocated to a
        domain. If domain is None, then this change the amount of memory reserved
        to Domain0 i.e. the domain where the application runs.
        This function may require privileged access to the hypervisor.
        
        This command only changes the runtime configuration of the domain,
        so can only be called on an active domain. """
        ret = libvirtmod.virDomainSetMemory(self._o, memory)
        if ret == -1: raise libvirtError ('virDomainSetMemory() failed', dom=self)
        return ret

    def setMemoryFlags(self, memory, flags=0):
        """Dynamically change the target amount of physical memory allocated to a
        domain. If domain is None, then this change the amount of memory reserved
        to Domain0 i.e. the domain where the application runs.
        This function may require privileged access to the hypervisor.
        
        @flags may include VIR_DOMAIN_AFFECT_LIVE or VIR_DOMAIN_AFFECT_CONFIG.
        Both flags may be set. If VIR_DOMAIN_AFFECT_LIVE is set, the change affects
        a running domain and will fail if domain is not active.
        If VIR_DOMAIN_AFFECT_CONFIG is set, the change affects persistent state,
        and will fail for transient domains. If neither flag is specified
        (that is, @flags is VIR_DOMAIN_AFFECT_CURRENT), then an inactive domain
        modifies persistent setup, while an active domain is hypervisor-dependent
        on whether just live or both live and persistent state is changed.
        If VIR_DOMAIN_MEM_MAXIMUM is set, the change affects domain's maximum memory
        size rather than current memory size.
        Not all hypervisors can support all flag combinations. """
        ret = libvirtmod.virDomainSetMemoryFlags(self._o, memory, flags)
        if ret == -1: raise libvirtError ('virDomainSetMemoryFlags() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def setMemoryParameters(self, params, flags=0):
        """Change the memory tunables """
        ret = libvirtmod.virDomainSetMemoryParameters(self._o, params, flags)
        if ret == -1: raise libvirtError ('virDomainSetMemoryParameters() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def setMemoryStatsPeriod(self, period, flags=0):
        """Dynamically change the domain memory balloon driver statistics collection
        period. Use 0 to disable and a positive value to enable.
        
        @flags may include VIR_DOMAIN_AFFECT_LIVE or VIR_DOMAIN_AFFECT_CONFIG.
        Both flags may be set. If VIR_DOMAIN_AFFECT_LIVE is set, the change affects
        a running domain and will fail if domain is not active.
        If VIR_DOMAIN_AFFECT_CONFIG is set, the change affects persistent state,
        and will fail for transient domains. If neither flag is specified
        (that is, @flags is VIR_DOMAIN_AFFECT_CURRENT), then an inactive domain
        modifies persistent setup, while an active domain is hypervisor-dependent
        on whether just live or both live and persistent state is changed.
        
        Not all hypervisors can support all flag combinations. """
        ret = libvirtmod.virDomainSetMemoryStatsPeriod(self._o, period, flags)
        if ret == -1: raise libvirtError ('virDomainSetMemoryStatsPeriod() failed', dom=self)
        return ret

    def setMetadata(self, type, metadata, key, uri, flags=0):
        """Sets the appropriate domain element given by @type to the
        value of @description.  A @type of VIR_DOMAIN_METADATA_DESCRIPTION
        is free-form text; VIR_DOMAIN_METADATA_TITLE is free-form, but no
        newlines are permitted, and should be short (although the length is
        not enforced). For these two options @key and @uri are irrelevant and
        must be set to None.
        
        For type VIR_DOMAIN_METADATA_ELEMENT @metadata  must be well-formed
        XML belonging to namespace defined by @uri with local name @key.
        
        Passing None for @metadata says to remove that element from the
        domain XML (passing the empty string leaves the element present).
        
        The resulting metadata will be present in virDomainGetXMLDesc(),
        as well as quick access through virDomainGetMetadata().
        
        @flags controls whether the live domain, persistent configuration,
        or both will be modified. """
        ret = libvirtmod.virDomainSetMetadata(self._o, type, metadata, key, uri, flags)
        if ret == -1: raise libvirtError ('virDomainSetMetadata() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def setNumaParameters(self, params, flags=0):
        """Change the NUMA tunables """
        ret = libvirtmod.virDomainSetNumaParameters(self._o, params, flags)
        if ret == -1: raise libvirtError ('virDomainSetNumaParameters() failed', dom=self)
        return ret

    def setSchedulerParameters(self, params):
        """Change the scheduler parameters """
        ret = libvirtmod.virDomainSetSchedulerParameters(self._o, params)
        if ret == -1: raise libvirtError ('virDomainSetSchedulerParameters() failed', dom=self)
        return ret

    def setSchedulerParametersFlags(self, params, flags=0):
        """Change the scheduler parameters """
        ret = libvirtmod.virDomainSetSchedulerParametersFlags(self._o, params, flags)
        if ret == -1: raise libvirtError ('virDomainSetSchedulerParametersFlags() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def setVcpus(self, nvcpus):
        """Dynamically change the number of virtual CPUs used by the domain.
        Note that this call may fail if the underlying virtualization hypervisor
        does not support it or if growing the number is arbitrary limited.
        This function may require privileged access to the hypervisor.
        
        This command only changes the runtime configuration of the domain,
        so can only be called on an active domain.  It is hypervisor-dependent
        whether it also affects persistent configuration; for more control,
        use virDomainSetVcpusFlags(). """
        ret = libvirtmod.virDomainSetVcpus(self._o, nvcpus)
        if ret == -1: raise libvirtError ('virDomainSetVcpus() failed', dom=self)
        return ret

    def setVcpusFlags(self, nvcpus, flags=0):
        """Dynamically change the number of virtual CPUs used by the domain.
        Note that this call may fail if the underlying virtualization hypervisor
        does not support it or if growing the number is arbitrary limited.
        This function may require privileged access to the hypervisor.
        
        @flags may include VIR_DOMAIN_AFFECT_LIVE to affect a running
        domain (which may fail if domain is not active), or
        VIR_DOMAIN_AFFECT_CONFIG to affect the next boot via the XML
        description of the domain.  Both flags may be set.
        If neither flag is specified (that is, @flags is VIR_DOMAIN_AFFECT_CURRENT),
        then an inactive domain modifies persistent setup, while an active domain
        is hypervisor-dependent on whether just live or both live and persistent
        state is changed.
        
        If @flags includes VIR_DOMAIN_VCPU_MAXIMUM, then
        VIR_DOMAIN_AFFECT_LIVE must be clear, and only the maximum virtual
        CPU limit is altered; generally, this value must be less than or
        equal to virConnectGetMaxVcpus().  Otherwise, this call affects the
        current virtual CPU limit, which must be less than or equal to the
        maximum limit.
        
        If @flags includes VIR_DOMAIN_VCPU_GUEST, then the state of processors is
        modified inside the guest instead of the hypervisor. This flag can only
        be used with live guests and is incompatible with VIR_DOMAIN_VCPU_MAXIMUM.
        The usage of this flag may require a guest agent configured.
        
        Not all hypervisors can support all flag combinations. """
        ret = libvirtmod.virDomainSetVcpusFlags(self._o, nvcpus, flags)
        if ret == -1: raise libvirtError ('virDomainSetVcpusFlags() failed', dom=self)
        return ret

    def shutdown(self):
        """Shutdown a domain, the domain object is still usable thereafter, but
        the domain OS is being stopped. Note that the guest OS may ignore the
        request. Additionally, the hypervisor may check and support the domain
        'on_poweroff' XML setting resulting in a domain that reboots instead of
        shutting down. For guests that react to a shutdown request, the differences
        from virDomainDestroy() are that the guests disk storage will be in a
        stable state rather than having the (virtual) power cord pulled, and
        this command returns as soon as the shutdown request is issued rather
        than blocking until the guest is no longer running.
        
        If the domain is transient and has any snapshot metadata (see
        virDomainSnapshotNum()), then that metadata will automatically
        be deleted when the domain quits. """
        ret = libvirtmod.virDomainShutdown(self._o)
        if ret == -1: raise libvirtError ('virDomainShutdown() failed', dom=self)
        return ret

    def shutdownFlags(self, flags=0):
        """Shutdown a domain, the domain object is still usable thereafter but
        the domain OS is being stopped. Note that the guest OS may ignore the
        request. Additionally, the hypervisor may check and support the domain
        'on_poweroff' XML setting resulting in a domain that reboots instead of
        shutting down. For guests that react to a shutdown request, the differences
        from virDomainDestroy() are that the guest's disk storage will be in a
        stable state rather than having the (virtual) power cord pulled, and
        this command returns as soon as the shutdown request is issued rather
        than blocking until the guest is no longer running.
        
        If the domain is transient and has any snapshot metadata (see
        virDomainSnapshotNum()), then that metadata will automatically
        be deleted when the domain quits.
        
        If @flags is set to zero, then the hypervisor will choose the
        method of shutdown it considers best. To have greater control
        pass one or more of the virDomainShutdownFlagValues. The order
        in which the hypervisor tries each shutdown method is undefined,
        and a hypervisor is not required to support all methods. """
        ret = libvirtmod.virDomainShutdownFlags(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainShutdownFlags() failed', dom=self)
        return ret

    def snapshotCreateXML(self, xmlDesc, flags=0):
        """Creates a new snapshot of a domain based on the snapshot xml
        contained in xmlDesc.
        
        If @flags is 0, the domain can be active, in which case the
        snapshot will be a system checkpoint (both disk state and runtime
        VM state such as RAM contents), where reverting to the snapshot is
        the same as resuming from hibernation (TCP connections may have
        timed out, but everything else picks up where it left off); or
        the domain can be inactive, in which case the snapshot includes
        just the disk state prior to booting.  The newly created snapshot
        becomes current (see virDomainSnapshotCurrent()), and is a child
        of any previous current snapshot.
        
        If @flags includes VIR_DOMAIN_SNAPSHOT_CREATE_REDEFINE, then this
        is a request to reinstate snapshot metadata that was previously
        discarded, rather than creating a new snapshot.  This can be used
        to recreate a snapshot hierarchy on a destination, then remove it
        on the source, in order to allow migration (since migration
        normally fails if snapshot metadata still remains on the source
        machine).  When redefining snapshot metadata, the current snapshot
        will not be altered unless the VIR_DOMAIN_SNAPSHOT_CREATE_CURRENT
        flag is also present.  It is an error to request the
        VIR_DOMAIN_SNAPSHOT_CREATE_CURRENT flag without
        VIR_DOMAIN_SNAPSHOT_CREATE_REDEFINE.  On some hypervisors,
        redefining an existing snapshot can be used to alter host-specific
        portions of the domain XML to be used during revert (such as
        backing filenames associated with disk devices), but must not alter
        guest-visible layout.  When redefining a snapshot name that does
        not exist, the hypervisor may validate that reverting to the
        snapshot appears to be possible (for example, disk images have
        snapshot contents by the requested name).  Not all hypervisors
        support these flags.
        
        If @flags includes VIR_DOMAIN_SNAPSHOT_CREATE_NO_METADATA, then the
        domain's disk images are modified according to @xmlDesc, but then
        the just-created snapshot has its metadata deleted.  This flag is
        incompatible with VIR_DOMAIN_SNAPSHOT_CREATE_REDEFINE.
        
        If @flags includes VIR_DOMAIN_SNAPSHOT_CREATE_HALT, then the domain
        will be inactive after the snapshot completes, regardless of whether
        it was active before; otherwise, a running domain will still be
        running after the snapshot.  This flag is invalid on transient domains,
        and is incompatible with VIR_DOMAIN_SNAPSHOT_CREATE_REDEFINE.
        
        If @flags includes VIR_DOMAIN_SNAPSHOT_CREATE_LIVE, then the domain
        is not paused while creating the snapshot. This increases the size
        of the memory dump file, but reduces downtime of the guest while
        taking the snapshot. Some hypervisors only support this flag during
        external checkpoints.
        
        If @flags includes VIR_DOMAIN_SNAPSHOT_CREATE_DISK_ONLY, then the
        snapshot will be limited to the disks described in @xmlDesc, and no
        VM state will be saved.  For an active guest, the disk image may be
        inconsistent (as if power had been pulled), and specifying this
        with the VIR_DOMAIN_SNAPSHOT_CREATE_HALT flag risks data loss.
        
        If @flags includes VIR_DOMAIN_SNAPSHOT_CREATE_QUIESCE, then the
        libvirt will attempt to use guest agent to freeze and thaw all
        file systems in use within domain OS. However, if the guest agent
        is not present, an error is thrown. Moreover, this flag requires
        VIR_DOMAIN_SNAPSHOT_CREATE_DISK_ONLY to be passed as well.
        
        By default, if the snapshot involves external files, and any of the
        destination files already exist as a non-empty regular file, the
        snapshot is rejected to avoid losing contents of those files.
        However, if @flags includes VIR_DOMAIN_SNAPSHOT_CREATE_REUSE_EXT,
        then the destination files must already exist and contain content
        identical to the source files (this allows a management app to
        pre-create files with relative backing file names, rather than the
        default of creating with absolute backing file names).
        
        Be aware that although libvirt prefers to report errors up front with
        no other effect, some hypervisors have certain types of failures where
        the overall command can easily fail even though the guest configuration
        was partially altered (for example, if a disk snapshot request for two
        disks fails on the second disk, but the first disk alteration cannot be
        rolled back).  If this API call fails, it is therefore normally
        necessary to follow up with virDomainGetXMLDesc() and check each disk
        to determine if any partial changes occurred.  However, if @flags
        contains VIR_DOMAIN_SNAPSHOT_CREATE_ATOMIC, then libvirt guarantees
        that this command will not alter any disks unless the entire set of
        changes can be done atomically, making failure recovery simpler (note
        that it is still possible to fail after disks have changed, but only
        in the much rarer cases of running out of memory or disk space).
        
        Some hypervisors may prevent this operation if there is a current
        block copy operation; in that case, use virDomainBlockJobAbort()
        to stop the block copy first. """
        ret = libvirtmod.virDomainSnapshotCreateXML(self._o, xmlDesc, flags)
        if ret is None:raise libvirtError('virDomainSnapshotCreateXML() failed', dom=self)
        __tmp = virDomainSnapshot(self,_obj=ret)
        return __tmp

    def snapshotCurrent(self, flags=0):
        """Get the current snapshot for a domain, if any. """
        ret = libvirtmod.virDomainSnapshotCurrent(self._o, flags)
        if ret is None:raise libvirtError('virDomainSnapshotCurrent() failed', dom=self)
        __tmp = virDomainSnapshot(self,_obj=ret)
        return __tmp

    #
    # virDomain functions from module python
    #

    def snapshotListNames(self, flags=0):
        """collect the list of snapshot names for the given domain """
        ret = libvirtmod.virDomainSnapshotListNames(self._o, flags)
        if ret is None: raise libvirtError ('virDomainSnapshotListNames() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def snapshotLookupByName(self, name, flags=0):
        """Try to lookup a domain snapshot based on its name. """
        ret = libvirtmod.virDomainSnapshotLookupByName(self._o, name, flags)
        if ret is None:raise libvirtError('virDomainSnapshotLookupByName() failed', dom=self)
        __tmp = virDomainSnapshot(self,_obj=ret)
        return __tmp

    def snapshotNum(self, flags=0):
        """Provides the number of domain snapshots for this domain.
        
        By default, this command covers all snapshots; it is also possible to
        limit things to just snapshots with no parents, when @flags includes
        VIR_DOMAIN_SNAPSHOT_LIST_ROOTS.  Additional filters are provided in
        groups, where each group contains bits that describe mutually exclusive
        attributes of a snapshot, and where all bits within a group describe
        all possible snapshots.  Some hypervisors might reject explicit bits
        from a group where the hypervisor cannot make a distinction.  For a
        group supported by a given hypervisor, the behavior when no bits of a
        group are set is identical to the behavior when all bits in that group
        are set.  When setting bits from more than one group, it is possible to
        select an impossible combination, in that case a hypervisor may return
        either 0 or an error.
        
        The first group of @flags is VIR_DOMAIN_SNAPSHOT_LIST_LEAVES and
        VIR_DOMAIN_SNAPSHOT_LIST_NO_LEAVES, to filter based on snapshots that
        have no further children (a leaf snapshot).
        
        The next group of @flags is VIR_DOMAIN_SNAPSHOT_LIST_METADATA and
        VIR_DOMAIN_SNAPSHOT_LIST_NO_METADATA, for filtering snapshots based on
        whether they have metadata that would prevent the removal of the last
        reference to a domain.
        
        The next group of @flags is VIR_DOMAIN_SNAPSHOT_LIST_INACTIVE,
        VIR_DOMAIN_SNAPSHOT_LIST_ACTIVE, and VIR_DOMAIN_SNAPSHOT_LIST_DISK_ONLY,
        for filtering snapshots based on what domain state is tracked by the
        snapshot.
        
        The next group of @flags is VIR_DOMAIN_SNAPSHOT_LIST_INTERNAL and
        VIR_DOMAIN_SNAPSHOT_LIST_EXTERNAL, for filtering snapshots based on
        whether the snapshot is stored inside the disk images or as
        additional files. """
        ret = libvirtmod.virDomainSnapshotNum(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainSnapshotNum() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def state(self, flags=0):
        """Extract domain state. """
        ret = libvirtmod.virDomainGetState(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetState() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def suspend(self):
        """Suspends an active domain, the process is frozen without further access
        to CPU resources and I/O but the memory used by the domain at the
        hypervisor level will stay allocated. Use virDomainResume() to reactivate
        the domain.
        This function may require privileged access.
        Moreover, suspend may not be supported if domain is in some
        special state like VIR_DOMAIN_PMSUSPENDED. """
        ret = libvirtmod.virDomainSuspend(self._o)
        if ret == -1: raise libvirtError ('virDomainSuspend() failed', dom=self)
        return ret

    def undefine(self):
        """Undefine a domain. If the domain is running, it's converted to
        transient domain, without stopping it. If the domain is inactive,
        the domain configuration is removed.
        
        If the domain has a managed save image (see
        virDomainHasManagedSaveImage()), or if it is inactive and has any
        snapshot metadata (see virDomainSnapshotNum()), then the undefine will
        fail. See virDomainUndefineFlags() for more control. """
        ret = libvirtmod.virDomainUndefine(self._o)
        if ret == -1: raise libvirtError ('virDomainUndefine() failed', dom=self)
        return ret

    def undefineFlags(self, flags=0):
        """Undefine a domain. If the domain is running, it's converted to
        transient domain, without stopping it. If the domain is inactive,
        the domain configuration is removed.
        
        If the domain has a managed save image (see virDomainHasManagedSaveImage()),
        then including VIR_DOMAIN_UNDEFINE_MANAGED_SAVE in @flags will also remove
        that file, and omitting the flag will cause the undefine process to fail.
        
        If the domain is inactive and has any snapshot metadata (see
        virDomainSnapshotNum()), then including
        VIR_DOMAIN_UNDEFINE_SNAPSHOTS_METADATA in @flags will also remove
        that metadata.  Omitting the flag will cause the undefine of an
        inactive domain to fail.  Active snapshots will retain snapshot
        metadata until the (now-transient) domain halts, regardless of
        whether this flag is present.  On hypervisors where snapshots do
        not use libvirt metadata, this flag has no effect. """
        ret = libvirtmod.virDomainUndefineFlags(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainUndefineFlags() failed', dom=self)
        return ret

    def updateDeviceFlags(self, xml, flags=0):
        """Change a virtual device on a domain, using the flags parameter
        to control how the device is changed.  VIR_DOMAIN_AFFECT_CURRENT
        specifies that the device change is made based on current domain
        state.  VIR_DOMAIN_AFFECT_LIVE specifies that the device shall be
        changed on the active domain instance only and is not added to the
        persisted domain configuration. VIR_DOMAIN_AFFECT_CONFIG
        specifies that the device shall be changed on the persisted domain
        configuration only.  Note that the target hypervisor must return an
        error if unable to satisfy flags.  E.g. the hypervisor driver will
        return failure if LIVE is specified but it only supports modifying the
        persisted device allocation.
        
        This method is used for actions such changing CDROM/Floppy device
        media, altering the graphics configuration such as password,
        reconfiguring the NIC device backend connectivity, etc. """
        ret = libvirtmod.virDomainUpdateDeviceFlags(self._o, xml, flags)
        if ret == -1: raise libvirtError ('virDomainUpdateDeviceFlags() failed', dom=self)
        return ret

    #
    # virDomain functions from module python
    #

    def vcpuPinInfo(self, flags=0):
        """Query the CPU affinity setting of all virtual CPUs of domain """
        ret = libvirtmod.virDomainGetVcpuPinInfo(self._o, flags)
        if ret is None: raise libvirtError ('virDomainGetVcpuPinInfo() failed', dom=self)
        return ret

    def vcpus(self):
        """Extract information about virtual CPUs of domain, store it in info array and also in cpumaps if this pointer is'nt None. """
        ret = libvirtmod.virDomainGetVcpus(self._o)
        if ret == -1: raise libvirtError ('virDomainGetVcpus() failed', dom=self)
        return ret

    #
    # virDomain functions from module libvirt
    #

    def vcpusFlags(self, flags=0):
        """Query the number of virtual CPUs used by the domain.  Note that
        this call may fail if the underlying virtualization hypervisor does
        not support it.  This function may require privileged access to the
        hypervisor.
        
        If @flags includes VIR_DOMAIN_AFFECT_LIVE, this will query a
        running domain (which will fail if domain is not active); if
        it includes VIR_DOMAIN_AFFECT_CONFIG, this will query the XML
        description of the domain.  It is an error to set both flags.
        If neither flag is set (that is, VIR_DOMAIN_AFFECT_CURRENT),
        then the configuration queried depends on whether the domain
        is currently running.
        
        If @flags includes VIR_DOMAIN_VCPU_MAXIMUM, then the maximum
        virtual CPU limit is queried.  Otherwise, this call queries the
        current virtual CPU count.
        
        If @flags includes VIR_DOMAIN_VCPU_GUEST, then the state of the processors
        is modified in the guest instead of the hypervisor. This flag is only usable
        on live domains. Guest agent may be needed for this flag to be available. """
        ret = libvirtmod.virDomainGetVcpusFlags(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainGetVcpusFlags() failed', dom=self)
        return ret

    #
    # virDomain methods from virDomain.py (hand coded)
    #
    def listAllSnapshots(self, flags=0):
        """List all snapshots and returns a list of snapshot objects"""
        ret = libvirtmod.virDomainListAllSnapshots(self._o, flags)
        if ret is None:
            raise libvirtError("virDomainListAllSnapshots() failed", conn=self)

        retlist = list()
        for snapptr in ret:
            retlist.append(virDomainSnapshot(self, _obj=snapptr))

        return retlist


    def createWithFiles(self, files, flags=0):
        """Launch a defined domain. If the call succeeds the domain moves from the
        defined to the running domains pools.

        @files provides an array of file descriptors which will be
        made available to the 'init' process of the guest. The file
        handles exposed to the guest will be renumbered to start
        from 3 (ie immediately following stderr). This is only
        supported for guests which use container based virtualization
        technology.

        If the VIR_DOMAIN_START_PAUSED flag is set, or if the guest domain
        has a managed save image that requested paused state (see
        virDomainManagedSave()) the guest domain will be started, but its
        CPUs will remain paused. The CPUs can later be manually started
        using virDomainResume().  In all other cases, the guest domain will
        be running.

        If the VIR_DOMAIN_START_AUTODESTROY flag is set, the guest
        domain will be automatically destroyed when the virConnectPtr
        object is finally released. This will also happen if the
        client application crashes / loses its connection to the
        libvirtd daemon. Any domains marked for auto destroy will
        block attempts at migration, save-to-file, or snapshots.

        If the VIR_DOMAIN_START_BYPASS_CACHE flag is set, and there is a
        managed save file for this domain (created by virDomainManagedSave()),
        then libvirt will attempt to bypass the file system cache while restoring
        the file, or fail if it cannot do so for the given system; this can allow
        less pressure on file system cache, but also risks slowing loads from NFS.

        If the VIR_DOMAIN_START_FORCE_BOOT flag is set, then any managed save
        file for this domain is discarded, and the domain boots from scratch. """
        ret = libvirtmod.virDomainCreateWithFiles(self._o, files, flags)
        if ret == -1: raise libvirtError ('virDomainCreateWithFiles() failed', dom=self)
        return ret

class virNetwork(object):
    def __init__(self, conn, _obj=None):
        self._conn = conn
        self._o = _obj

    def __del__(self):
        if self._o is not None:
            libvirtmod.virNetworkFree(self._o)
        self._o = None

    def connect(self):
        return self._conn

    #
    # virNetwork functions from module python
    #

    def UUID(self):
        """Extract the UUID unique Identifier of a network. """
        ret = libvirtmod.virNetworkGetUUID(self._o)
        if ret is None: raise libvirtError ('virNetworkGetUUID() failed', net=self)
        return ret

    def UUIDString(self):
        """Fetch globally unique ID of the network as a string. """
        ret = libvirtmod.virNetworkGetUUIDString(self._o)
        if ret is None: raise libvirtError ('virNetworkGetUUIDString() failed', net=self)
        return ret

    #
    # virNetwork functions from module libvirt
    #

    def XMLDesc(self, flags=0):
        """Provide an XML description of the network. The description may be reused
        later to relaunch the network with virNetworkCreateXML().
        
        Normally, if a network included a physical function, the output includes
        all virtual functions tied to that physical interface.  If @flags includes
        VIR_NETWORK_XML_INACTIVE, then the expansion of virtual interfaces is
        not performed. """
        ret = libvirtmod.virNetworkGetXMLDesc(self._o, flags)
        if ret is None: raise libvirtError ('virNetworkGetXMLDesc() failed', net=self)
        return ret

    #
    # virNetwork functions from module python
    #

    def autostart(self):
        """Extract the autostart flag for a network. """
        ret = libvirtmod.virNetworkGetAutostart(self._o)
        if ret == -1: raise libvirtError ('virNetworkGetAutostart() failed', net=self)
        return ret

    #
    # virNetwork functions from module libvirt
    #

    def bridgeName(self):
        """Provides a bridge interface name to which a domain may connect
        a network interface in order to join the network. """
        ret = libvirtmod.virNetworkGetBridgeName(self._o)
        if ret is None: raise libvirtError ('virNetworkGetBridgeName() failed', net=self)
        return ret

    def create(self):
        """Create and start a defined network. If the call succeed the network
        moves from the defined to the running networks pools. """
        ret = libvirtmod.virNetworkCreate(self._o)
        if ret == -1: raise libvirtError ('virNetworkCreate() failed', net=self)
        return ret

    def destroy(self):
        """Destroy the network object. The running instance is shutdown if not down
        already and all resources used by it are given back to the hypervisor. This
        does not free the associated virNetworkPtr object.
        This function may require privileged access """
        ret = libvirtmod.virNetworkDestroy(self._o)
        if ret == -1: raise libvirtError ('virNetworkDestroy() failed', net=self)
        return ret

    def isActive(self):
        """Determine if the network is currently running """
        ret = libvirtmod.virNetworkIsActive(self._o)
        if ret == -1: raise libvirtError ('virNetworkIsActive() failed', net=self)
        return ret

    def isPersistent(self):
        """Determine if the network has a persistent configuration
        which means it will still exist after shutting down """
        ret = libvirtmod.virNetworkIsPersistent(self._o)
        if ret == -1: raise libvirtError ('virNetworkIsPersistent() failed', net=self)
        return ret

    def name(self):
        """Get the public name for that network """
        ret = libvirtmod.virNetworkGetName(self._o)
        return ret

    def setAutostart(self, autostart):
        """Configure the network to be automatically started
        when the host machine boots. """
        ret = libvirtmod.virNetworkSetAutostart(self._o, autostart)
        if ret == -1: raise libvirtError ('virNetworkSetAutostart() failed', net=self)
        return ret

    def undefine(self):
        """Undefine a network but does not stop it if it is running """
        ret = libvirtmod.virNetworkUndefine(self._o)
        if ret == -1: raise libvirtError ('virNetworkUndefine() failed', net=self)
        return ret

    def update(self, command, section, parentIndex, xml, flags=0):
        """Update the definition of an existing network, either its live
        running state, its persistent configuration, or both. """
        ret = libvirtmod.virNetworkUpdate(self._o, command, section, parentIndex, xml, flags)
        if ret == -1: raise libvirtError ('virNetworkUpdate() failed', net=self)
        return ret

class virInterface(object):
    def __init__(self, conn, _obj=None):
        self._conn = conn
        self._o = _obj

    def __del__(self):
        if self._o is not None:
            libvirtmod.virInterfaceFree(self._o)
        self._o = None

    def connect(self):
        return self._conn

    #
    # virInterface functions from module libvirt
    #

    def MACString(self):
        """Get the MAC for an interface as string. For more information about
        MAC see RFC4122. """
        ret = libvirtmod.virInterfaceGetMACString(self._o)
        if ret is None: raise libvirtError ('virInterfaceGetMACString() failed', net=self)
        return ret

    def XMLDesc(self, flags=0):
        """VIR_INTERFACE_XML_INACTIVE - return the static configuration,
                                          suitable for use redefining the
                                          interface via virInterfaceDefineXML()
        
        Provide an XML description of the interface. If
        VIR_INTERFACE_XML_INACTIVE is set, the description may be reused
        later to redefine the interface with virInterfaceDefineXML(). If it
        is not set, the ip address and netmask will be the current live
        setting of the interface, not the settings from the config files. """
        ret = libvirtmod.virInterfaceGetXMLDesc(self._o, flags)
        if ret is None: raise libvirtError ('virInterfaceGetXMLDesc() failed', net=self)
        return ret

    def create(self, flags=0):
        """Activate an interface (i.e. call "ifup").
        
        If there was an open network config transaction at the time this
        interface was defined (that is, if virInterfaceChangeBegin() had
        been called), the interface will be brought back down (and then
        undefined) if virInterfaceChangeRollback() is called. """
        ret = libvirtmod.virInterfaceCreate(self._o, flags)
        if ret == -1: raise libvirtError ('virInterfaceCreate() failed', net=self)
        return ret

    def destroy(self, flags=0):
        """deactivate an interface (ie call "ifdown")
        This does not remove the interface from the config, and
        does not free the associated virInterfacePtr object.
        
        If there is an open network config transaction at the time this
        interface is destroyed (that is, if virInterfaceChangeBegin() had
        been called), and if the interface is later undefined and then
        virInterfaceChangeRollback() is called, the restoral of the
        interface definition will also bring the interface back up. """
        ret = libvirtmod.virInterfaceDestroy(self._o, flags)
        if ret == -1: raise libvirtError ('virInterfaceDestroy() failed', net=self)
        return ret

    def isActive(self):
        """Determine if the interface is currently running """
        ret = libvirtmod.virInterfaceIsActive(self._o)
        if ret == -1: raise libvirtError ('virInterfaceIsActive() failed', net=self)
        return ret

    def name(self):
        """Get the public name for that interface """
        ret = libvirtmod.virInterfaceGetName(self._o)
        return ret

    def undefine(self):
        """Undefine an interface, ie remove it from the config.
        This does not free the associated virInterfacePtr object.
        
        Normally this change in the interface configuration is
        permanent/persistent, but if virInterfaceChangeBegin() has been
        previously called (i.e. if an interface config transaction is
        open), the removal of the interface definition will only become
        permanent if virInterfaceChangeCommit() is called prior to the next
        reboot of the system running libvirtd. Prior to that time, the
        definition can be explicitly restored using
        virInterfaceChangeRollback(), or will be automatically restored
        during the next reboot of the system running libvirtd. """
        ret = libvirtmod.virInterfaceUndefine(self._o)
        if ret == -1: raise libvirtError ('virInterfaceUndefine() failed', net=self)
        return ret

class virStoragePool(object):
    def __init__(self, conn, _obj=None):
        self._conn = conn
        if not isinstance(conn, virConnect):
            self._conn = conn._conn
        self._o = _obj

    def __del__(self):
        if self._o is not None:
            libvirtmod.virStoragePoolFree(self._o)
        self._o = None

    def connect(self):
        return self._conn

    #
    # virStoragePool functions from module python
    #

    def UUID(self):
        """Extract the UUID unique Identifier of a storage pool. """
        ret = libvirtmod.virStoragePoolGetUUID(self._o)
        if ret is None: raise libvirtError ('virStoragePoolGetUUID() failed', pool=self)
        return ret

    def UUIDString(self):
        """Fetch globally unique ID of the storage pool as a string. """
        ret = libvirtmod.virStoragePoolGetUUIDString(self._o)
        if ret is None: raise libvirtError ('virStoragePoolGetUUIDString() failed', pool=self)
        return ret

    #
    # virStoragePool functions from module libvirt
    #

    def XMLDesc(self, flags=0):
        """Fetch an XML document describing all aspects of the
        storage pool. This is suitable for later feeding back
        into the virStoragePoolCreateXML method. """
        ret = libvirtmod.virStoragePoolGetXMLDesc(self._o, flags)
        if ret is None: raise libvirtError ('virStoragePoolGetXMLDesc() failed', pool=self)
        return ret

    #
    # virStoragePool functions from module python
    #

    def autostart(self):
        """Extract the autostart flag for a storage pool """
        ret = libvirtmod.virStoragePoolGetAutostart(self._o)
        if ret == -1: raise libvirtError ('virStoragePoolGetAutostart() failed', pool=self)
        return ret

    #
    # virStoragePool functions from module libvirt
    #

    def build(self, flags=0):
        """Currently only filesystem pool accepts flags VIR_STORAGE_POOL_BUILD_OVERWRITE
        and VIR_STORAGE_POOL_BUILD_NO_OVERWRITE.
        
        Build the underlying storage pool """
        ret = libvirtmod.virStoragePoolBuild(self._o, flags)
        if ret == -1: raise libvirtError ('virStoragePoolBuild() failed', pool=self)
        return ret

    def create(self, flags=0):
        """Starts an inactive storage pool """
        ret = libvirtmod.virStoragePoolCreate(self._o, flags)
        if ret == -1: raise libvirtError ('virStoragePoolCreate() failed', pool=self)
        return ret

    def createXML(self, xmlDesc, flags=0):
        """Create a storage volume within a pool based
        on an XML description. Not all pools support
        creation of volumes.
        
        Since 1.0.1 VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA
        in flags can be used to get higher performance with
        qcow2 image files which don't support full preallocation,
        by creating a sparse image file with metadata. """
        ret = libvirtmod.virStorageVolCreateXML(self._o, xmlDesc, flags)
        if ret is None:raise libvirtError('virStorageVolCreateXML() failed', pool=self)
        __tmp = virStorageVol(self, _obj=ret)
        return __tmp

    def createXMLFrom(self, xmlDesc, clonevol, flags=0):
        """Create a storage volume in the parent pool, using the
        'clonevol' volume as input. Information for the new
        volume (name, perms)  are passed via a typical volume
        XML description.
        
        Since 1.0.1 VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA
        in flags can be used to get higher performance with
        qcow2 image files which don't support full preallocation,
        by creating a sparse image file with metadata. """
        if clonevol is None: clonevol__o = None
        else: clonevol__o = clonevol._o
        ret = libvirtmod.virStorageVolCreateXMLFrom(self._o, xmlDesc, clonevol__o, flags)
        if ret is None:raise libvirtError('virStorageVolCreateXMLFrom() failed', pool=self)
        __tmp = virStorageVol(self, _obj=ret)
        return __tmp

    def delete(self, flags=0):
        """Delete the underlying pool resources. This is
        a non-recoverable operation. The virStoragePoolPtr object
        itself is not free'd. """
        ret = libvirtmod.virStoragePoolDelete(self._o, flags)
        if ret == -1: raise libvirtError ('virStoragePoolDelete() failed', pool=self)
        return ret

    def destroy(self):
        """Destroy an active storage pool. This will deactivate the
        pool on the host, but keep any persistent config associated
        with it. If it has a persistent config it can later be
        restarted with virStoragePoolCreate(). This does not free
        the associated virStoragePoolPtr object. """
        ret = libvirtmod.virStoragePoolDestroy(self._o)
        if ret == -1: raise libvirtError ('virStoragePoolDestroy() failed', pool=self)
        return ret

    #
    # virStoragePool functions from module python
    #

    def info(self):
        """Extract information about a storage pool. Note that if the connection used to get the domain is limited only a partial set of the information can be extracted. """
        ret = libvirtmod.virStoragePoolGetInfo(self._o)
        if ret is None: raise libvirtError ('virStoragePoolGetInfo() failed', pool=self)
        return ret

    #
    # virStoragePool functions from module libvirt
    #

    def isActive(self):
        """Determine if the storage pool is currently running """
        ret = libvirtmod.virStoragePoolIsActive(self._o)
        if ret == -1: raise libvirtError ('virStoragePoolIsActive() failed', pool=self)
        return ret

    def isPersistent(self):
        """Determine if the storage pool has a persistent configuration
        which means it will still exist after shutting down """
        ret = libvirtmod.virStoragePoolIsPersistent(self._o)
        if ret == -1: raise libvirtError ('virStoragePoolIsPersistent() failed', pool=self)
        return ret

    #
    # virStoragePool functions from module python
    #

    def listVolumes(self):
        """list the storage volumes, stores the pointers to the names in @names """
        ret = libvirtmod.virStoragePoolListVolumes(self._o)
        if ret is None: raise libvirtError ('virStoragePoolListVolumes() failed', pool=self)
        return ret

    #
    # virStoragePool functions from module libvirt
    #

    def name(self):
        """Fetch the locally unique name of the storage pool """
        ret = libvirtmod.virStoragePoolGetName(self._o)
        return ret

    def numOfVolumes(self):
        """Fetch the number of storage volumes within a pool """
        ret = libvirtmod.virStoragePoolNumOfVolumes(self._o)
        if ret == -1: raise libvirtError ('virStoragePoolNumOfVolumes() failed', pool=self)
        return ret

    def refresh(self, flags=0):
        """Request that the pool refresh its list of volumes. This may
        involve communicating with a remote server, and/or initializing
        new devices at the OS layer """
        ret = libvirtmod.virStoragePoolRefresh(self._o, flags)
        if ret == -1: raise libvirtError ('virStoragePoolRefresh() failed', pool=self)
        return ret

    def setAutostart(self, autostart):
        """Sets the autostart flag """
        ret = libvirtmod.virStoragePoolSetAutostart(self._o, autostart)
        if ret == -1: raise libvirtError ('virStoragePoolSetAutostart() failed', pool=self)
        return ret

    def storageVolLookupByName(self, name):
        """Fetch a pointer to a storage volume based on its name
        within a pool """
        ret = libvirtmod.virStorageVolLookupByName(self._o, name)
        if ret is None:raise libvirtError('virStorageVolLookupByName() failed', pool=self)
        __tmp = virStorageVol(self, _obj=ret)
        return __tmp

    def undefine(self):
        """Undefine an inactive storage pool """
        ret = libvirtmod.virStoragePoolUndefine(self._o)
        if ret == -1: raise libvirtError ('virStoragePoolUndefine() failed', pool=self)
        return ret

    #
    # virStoragePool methods from virStoragePool.py (hand coded)
    #
    def listAllVolumes(self, flags=0):
        """List all storage volumes and returns a list of storage volume objects"""
        ret = libvirtmod.virStoragePoolListAllVolumes(self._o, flags)
        if ret is None:
            raise libvirtError("virStoragePoolListAllVolumes() failed", conn=self)

        retlist = list()
        for volptr in ret:
            retlist.append(virStorageVol(self, _obj=volptr))

        return retlist

class virStorageVol(object):
    def __init__(self, conn, _obj=None):
        self._conn = conn
        if not isinstance(conn, virConnect):
            self._conn = conn._conn
        self._o = _obj

    def __del__(self):
        if self._o is not None:
            libvirtmod.virStorageVolFree(self._o)
        self._o = None

    def connect(self):
        return self._conn

    #
    # virStorageVol functions from module libvirt
    #

    def XMLDesc(self, flags=0):
        """Fetch an XML document describing all aspects of
        the storage volume """
        ret = libvirtmod.virStorageVolGetXMLDesc(self._o, flags)
        if ret is None: raise libvirtError ('virStorageVolGetXMLDesc() failed', vol=self)
        return ret

    def delete(self, flags=0):
        """Delete the storage volume from the pool """
        ret = libvirtmod.virStorageVolDelete(self._o, flags)
        if ret == -1: raise libvirtError ('virStorageVolDelete() failed', vol=self)
        return ret

    def download(self, stream, offset, length, flags=0):
        """Download the content of the volume as a stream. If @length
        is zero, then the remaining contents of the volume after
        @offset will be downloaded.
        
        This call sets up an asynchronous stream; subsequent use of
        stream APIs is necessary to transfer the actual data,
        determine how much data is successfully transferred, and
        detect any errors. The results will be unpredictable if
        another active stream is writing to the storage volume. """
        if stream is None: stream__o = None
        else: stream__o = stream._o
        ret = libvirtmod.virStorageVolDownload(self._o, stream__o, offset, length, flags)
        if ret == -1: raise libvirtError ('virStorageVolDownload() failed', vol=self)
        return ret

    #
    # virStorageVol functions from module python
    #

    def info(self):
        """Extract information about a storage volume. Note that if the connection used to get the domain is limited only a partial set of the information can be extracted. """
        ret = libvirtmod.virStorageVolGetInfo(self._o)
        if ret is None: raise libvirtError ('virStorageVolGetInfo() failed', vol=self)
        return ret

    #
    # virStorageVol functions from module libvirt
    #

    def key(self):
        """Fetch the storage volume key. This is globally
        unique, so the same volume will have the same
        key no matter what host it is accessed from """
        ret = libvirtmod.virStorageVolGetKey(self._o)
        if ret is None: raise libvirtError ('virStorageVolGetKey() failed', vol=self)
        return ret

    def name(self):
        """Fetch the storage volume name. This is unique
        within the scope of a pool """
        ret = libvirtmod.virStorageVolGetName(self._o)
        return ret

    def path(self):
        """Fetch the storage volume path. Depending on the pool
        configuration this is either persistent across hosts,
        or dynamically assigned at pool startup. Consult
        pool documentation for information on getting the
        persistent naming """
        ret = libvirtmod.virStorageVolGetPath(self._o)
        if ret is None: raise libvirtError ('virStorageVolGetPath() failed', vol=self)
        return ret

    def resize(self, capacity, flags=0):
        """Changes the capacity of the storage volume @vol to @capacity. The
        operation will fail if the new capacity requires allocation that would
        exceed the remaining free space in the parent pool.  The contents of
        the new capacity will appear as all zero bytes. The capacity value will
        be rounded to the granularity supported by the hypervisor.
        
        Normally, the operation will attempt to affect capacity with a minimum
        impact on allocation (that is, the default operation favors a sparse
        resize).  If @flags contains VIR_STORAGE_VOL_RESIZE_ALLOCATE, then the
        operation will ensure that allocation is sufficient for the new
        capacity; this may make the operation take noticeably longer.
        
        Normally, the operation treats @capacity as the new size in bytes;
        but if @flags contains VIR_STORAGE_VOL_RESIZE_DELTA, then @capacity
        represents the size difference to add to the current size.  It is
        up to the storage pool implementation whether unaligned requests are
        rounded up to the next valid boundary, or rejected.
        
        Normally, this operation should only be used to enlarge capacity;
        but if @flags contains VIR_STORAGE_VOL_RESIZE_SHRINK, it is possible to
        attempt a reduction in capacity even though it might cause data loss.
        If VIR_STORAGE_VOL_RESIZE_DELTA is also present, then @capacity is
        subtracted from the current size; without it, @capacity represents
        the absolute new size regardless of whether it is larger or smaller
        than the current size. """
        ret = libvirtmod.virStorageVolResize(self._o, capacity, flags)
        if ret == -1: raise libvirtError ('virStorageVolResize() failed', vol=self)
        return ret

    def storagePoolLookupByVolume(self):
        """Fetch a storage pool which contains a particular volume """
        ret = libvirtmod.virStoragePoolLookupByVolume(self._o)
        if ret is None:raise libvirtError('virStoragePoolLookupByVolume() failed', vol=self)
        __tmp = virStoragePool(self, _obj=ret)
        return __tmp

    def upload(self, stream, offset, length, flags=0):
        """Upload new content to the volume from a stream. This call
        will fail if @offset + @length exceeds the size of the
        volume. Otherwise, if @length is non-zero, an error
        will be raised if an attempt is made to upload greater
        than @length bytes of data.
        
        This call sets up an asynchronous stream; subsequent use of
        stream APIs is necessary to transfer the actual data,
        determine how much data is successfully transferred, and
        detect any errors. The results will be unpredictable if
        another active stream is writing to the storage volume. """
        if stream is None: stream__o = None
        else: stream__o = stream._o
        ret = libvirtmod.virStorageVolUpload(self._o, stream__o, offset, length, flags)
        if ret == -1: raise libvirtError ('virStorageVolUpload() failed', vol=self)
        return ret

    def wipe(self, flags=0):
        """Ensure data previously on a volume is not accessible to future reads """
        ret = libvirtmod.virStorageVolWipe(self._o, flags)
        if ret == -1: raise libvirtError ('virStorageVolWipe() failed', vol=self)
        return ret

    def wipePattern(self, algorithm, flags=0):
        """Similar to virStorageVolWipe, but one can choose
        between different wiping algorithms. """
        ret = libvirtmod.virStorageVolWipePattern(self._o, algorithm, flags)
        if ret == -1: raise libvirtError ('virStorageVolWipePattern() failed', vol=self)
        return ret

class virConnect(object):
    def __init__(self, _obj=None):
        self._o = _obj

    #
    # virConnect functions from module python
    #

    def baselineCPU(self, xmlCPUs, flags=0):
        """Computes the most feature-rich CPU which is compatible with all given host CPUs. """
        ret = libvirtmod.virConnectBaselineCPU(self._o, xmlCPUs, flags)
        if ret is None: raise libvirtError ('virConnectBaselineCPU() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def changeBegin(self, flags=0):
        """This function creates a restore point to which one can return
        later by calling virInterfaceChangeRollback(). This function should
        be called before any transaction with interface configuration.
        Once it is known that a new configuration works, it can be committed via
        virInterfaceChangeCommit(), which frees the restore point.
        
        If virInterfaceChangeBegin() is called when a transaction is
        already opened, this function will fail, and a
        VIR_ERR_INVALID_OPERATION will be logged. """
        ret = libvirtmod.virInterfaceChangeBegin(self._o, flags)
        if ret == -1: raise libvirtError ('virInterfaceChangeBegin() failed', conn=self)
        return ret

    def changeCommit(self, flags=0):
        """This commits the changes made to interfaces and frees the restore point
        created by virInterfaceChangeBegin().
        
        If virInterfaceChangeCommit() is called when a transaction is not
        opened, this function will fail, and a VIR_ERR_INVALID_OPERATION
        will be logged. """
        ret = libvirtmod.virInterfaceChangeCommit(self._o, flags)
        if ret == -1: raise libvirtError ('virInterfaceChangeCommit() failed', conn=self)
        return ret

    def changeRollback(self, flags=0):
        """This cancels changes made to interfaces settings by restoring previous
        state created by virInterfaceChangeBegin().
        
        If virInterfaceChangeRollback() is called when a transaction is not
        opened, this function will fail, and a VIR_ERR_INVALID_OPERATION
        will be logged. """
        ret = libvirtmod.virInterfaceChangeRollback(self._o, flags)
        if ret == -1: raise libvirtError ('virInterfaceChangeRollback() failed', conn=self)
        return ret

    def close(self):
        """This function closes the connection to the Hypervisor. This should
        not be called if further interaction with the Hypervisor are needed
        especially if there is running domain which need further monitoring by
        the application.
        
        Connections are reference counted; the count is explicitly
        increased by the initial open (virConnectOpen, virConnectOpenAuth,
        and the like) as well as virConnectRef; it is also temporarily
        increased by other API that depend on the connection remaining
        alive.  The open and every virConnectRef call should have a
        matching virConnectClose, and all other references will be released
        after the corresponding operation completes. """
        ret = libvirtmod.virConnectClose(self._o)
        self._o = None
        if ret == -1: raise libvirtError ('virConnectClose() failed', conn=self)
        return ret

    def compareCPU(self, xmlDesc, flags=0):
        """Compares the given CPU description with the host CPU """
        ret = libvirtmod.virConnectCompareCPU(self._o, xmlDesc, flags)
        if ret == -1: raise libvirtError ('virConnectCompareCPU() failed', conn=self)
        return ret

    def createLinux(self, xmlDesc, flags=0):
        """Deprecated after 0.4.6.
        Renamed to virDomainCreateXML() providing identical functionality.
        This existing name will left indefinitely for API compatibility. """
        ret = libvirtmod.virDomainCreateLinux(self._o, xmlDesc, flags)
        if ret is None:raise libvirtError('virDomainCreateLinux() failed', conn=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    def createXML(self, xmlDesc, flags=0):
        """Launch a new guest domain, based on an XML description similar
        to the one returned by virDomainGetXMLDesc()
        This function may require privileged access to the hypervisor.
        The domain is not persistent, so its definition will disappear when it
        is destroyed, or if the host is restarted (see virDomainDefineXML() to
        define persistent domains).
        
        If the VIR_DOMAIN_START_PAUSED flag is set, the guest domain
        will be started, but its CPUs will remain paused. The CPUs
        can later be manually started using virDomainResume.
        
        If the VIR_DOMAIN_START_AUTODESTROY flag is set, the guest
        domain will be automatically destroyed when the virConnectPtr
        object is finally released. This will also happen if the
        client application crashes / loses its connection to the
        libvirtd daemon. Any domains marked for auto destroy will
        block attempts at migration, save-to-file, or snapshots. """
        ret = libvirtmod.virDomainCreateXML(self._o, xmlDesc, flags)
        if ret is None:raise libvirtError('virDomainCreateXML() failed', conn=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    def defineXML(self, xml):
        """Define a domain, but does not start it.
        This definition is persistent, until explicitly undefined with
        virDomainUndefine(). A previous definition for this domain would be
        overridden if it already exists.
        
        Some hypervisors may prevent this operation if there is a current
        block copy operation on a transient domain with the same id as the
        domain being defined; in that case, use virDomainBlockJobAbort() to
        stop the block copy first. """
        ret = libvirtmod.virDomainDefineXML(self._o, xml)
        if ret is None:raise libvirtError('virDomainDefineXML() failed', conn=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    def domainXMLFromNative(self, nativeFormat, nativeConfig, flags=0):
        """Reads native configuration data  describing a domain, and
        generates libvirt domain XML. The format of the native
        data is hypervisor dependant. """
        ret = libvirtmod.virConnectDomainXMLFromNative(self._o, nativeFormat, nativeConfig, flags)
        if ret is None: raise libvirtError ('virConnectDomainXMLFromNative() failed', conn=self)
        return ret

    def domainXMLToNative(self, nativeFormat, domainXml, flags=0):
        """Reads a domain XML configuration document, and generates
        a native configuration file describing the domain.
        The format of the native data is hypervisor dependant. """
        ret = libvirtmod.virConnectDomainXMLToNative(self._o, nativeFormat, domainXml, flags)
        if ret is None: raise libvirtError ('virConnectDomainXMLToNative() failed', conn=self)
        return ret

    def findStoragePoolSources(self, type, srcSpec, flags=0):
        """Talks to a storage backend and attempts to auto-discover the set of
        available storage pool sources. e.g. For iSCSI this would be a set of
        iSCSI targets. For NFS this would be a list of exported paths.  The
        srcSpec (optional for some storage pool types, e.g. local ones) is
        an instance of the storage pool's source element specifying where
        to look for the pools.
        
        srcSpec is not required for some types (e.g., those querying
        local storage resources only) """
        ret = libvirtmod.virConnectFindStoragePoolSources(self._o, type, srcSpec, flags)
        if ret is None: raise libvirtError ('virConnectFindStoragePoolSources() failed', conn=self)
        return ret

    #
    # virConnect functions from module python
    #

    def getCPUMap(self, flags=0):
        """Get node CPU information """
        ret = libvirtmod.virNodeGetCPUMap(self._o, flags)
        if ret is None: raise libvirtError ('virNodeGetCPUMap() failed', conn=self)
        return ret

    def getCPUModelNames(self, arch, flags=0):
        """Get the list of supported CPU models. """
        ret = libvirtmod.virConnectGetCPUModelNames(self._o, arch, flags)
        if ret is None: raise libvirtError ('virConnectGetCPUModelNames() failed', conn=self)
        return ret

    def getCPUStats(self, cpuNum, flags=0):
        """Extract node's CPU statistics. """
        ret = libvirtmod.virNodeGetCPUStats(self._o, cpuNum, flags)
        if ret is None: raise libvirtError ('virNodeGetCPUStats() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def getCapabilities(self):
        """Provides capabilities of the hypervisor / driver. """
        ret = libvirtmod.virConnectGetCapabilities(self._o)
        if ret is None: raise libvirtError ('virConnectGetCapabilities() failed', conn=self)
        return ret

    #
    # virConnect functions from module python
    #

    def getCellsFreeMemory(self, startCell, maxCells):
        """Returns the available memory for a list of cells """
        ret = libvirtmod.virNodeGetCellsFreeMemory(self._o, startCell, maxCells)
        if ret is None: raise libvirtError ('virNodeGetCellsFreeMemory() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def getFreeMemory(self):
        """provides the free memory available on the Node
        Note: most libvirt APIs provide memory sizes in kibibytes, but in this
        function the returned value is in bytes. Divide by 1024 as necessary. """
        ret = libvirtmod.virNodeGetFreeMemory(self._o)
        return ret

    def getHostname(self):
        """This returns a system hostname on which the hypervisor is
        running (based on the result of the gethostname system call, but
        possibly expanded to a fully-qualified domain name via getaddrinfo).
        If we are connected to a remote system, then this returns the
        hostname of the remote system. """
        ret = libvirtmod.virConnectGetHostname(self._o)
        if ret is None: raise libvirtError ('virConnectGetHostname() failed', conn=self)
        return ret

    #
    # virConnect functions from module python
    #

    def getInfo(self):
        """Extract hardware information about the Node. Note that the memory size is reported in MiB instead of KiB. """
        ret = libvirtmod.virNodeGetInfo(self._o)
        if ret is None: raise libvirtError ('virNodeGetInfo() failed', conn=self)
        return ret

    def getLibVersion(self):
        """Returns the libvirt version of the connection host """
        ret = libvirtmod.virConnectGetLibVersion(self._o)
        if ret == -1: raise libvirtError ('virConnectGetLibVersion() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def getMaxVcpus(self, type):
        """Provides the maximum number of virtual CPUs supported for a guest VM of a
        specific type. The 'type' parameter here corresponds to the 'type'
        attribute in the <domain> element of the XML. """
        ret = libvirtmod.virConnectGetMaxVcpus(self._o, type)
        if ret == -1: raise libvirtError ('virConnectGetMaxVcpus() failed', conn=self)
        return ret

    #
    # virConnect functions from module python
    #

    def getMemoryParameters(self, flags=0):
        """Get the node memory parameters """
        ret = libvirtmod.virNodeGetMemoryParameters(self._o, flags)
        if ret is None: raise libvirtError ('virNodeGetMemoryParameters() failed', conn=self)
        return ret

    def getMemoryStats(self, cellNum, flags=0):
        """Extract node's memory statistics. """
        ret = libvirtmod.virNodeGetMemoryStats(self._o, cellNum, flags)
        if ret is None: raise libvirtError ('virNodeGetMemoryStats() failed', conn=self)
        return ret

    def getSecurityModel(self):
        """Extract information about the host security model """
        ret = libvirtmod.virNodeGetSecurityModel(self._o)
        if ret is None: raise libvirtError ('virNodeGetSecurityModel() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def getSysinfo(self, flags=0):
        """This returns the XML description of the sysinfo details for the
        host on which the hypervisor is running, in the same format as the
        <sysinfo> element of a domain XML.  This information is generally
        available only for hypervisors running with root privileges. """
        ret = libvirtmod.virConnectGetSysinfo(self._o, flags)
        if ret is None: raise libvirtError ('virConnectGetSysinfo() failed', conn=self)
        return ret

    def getType(self):
        """Get the name of the Hypervisor driver used. This is merely the driver
        name; for example, both KVM and QEMU guests are serviced by the
        driver for the qemu:// URI, so a return of "QEMU" does not indicate
        whether KVM acceleration is present.  For more details about the
        hypervisor, use virConnectGetCapabilities(). """
        ret = libvirtmod.virConnectGetType(self._o)
        if ret is None: raise libvirtError ('virConnectGetType() failed', conn=self)
        return ret

    def getURI(self):
        """This returns the URI (name) of the hypervisor connection.
        Normally this is the same as or similar to the string passed
        to the virConnectOpen/virConnectOpenReadOnly call, but
        the driver may make the URI canonical.  If name == None
        was passed to virConnectOpen, then the driver will return
        a non-None URI which can be used to connect to the same
        hypervisor later. """
        ret = libvirtmod.virConnectGetURI(self._o)
        if ret is None: raise libvirtError ('virConnectGetURI() failed', conn=self)
        return ret

    #
    # virConnect functions from module python
    #

    def getVersion(self):
        """Returns the running hypervisor version of the connection host """
        ret = libvirtmod.virConnectGetVersion(self._o)
        if ret == -1: raise libvirtError ('virConnectGetVersion() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def interfaceDefineXML(self, xml, flags=0):
        """Define an interface (or modify existing interface configuration).
        
        Normally this change in the interface configuration is immediately
        permanent/persistent, but if virInterfaceChangeBegin() has been
        previously called (i.e. if an interface config transaction is
        open), the new interface definition will only become permanent if
        virInterfaceChangeCommit() is called prior to the next reboot of
        the system running libvirtd. Prior to that time, it can be
        explicitly removed using virInterfaceChangeRollback(), or will be
        automatically removed during the next reboot of the system running
        libvirtd. """
        ret = libvirtmod.virInterfaceDefineXML(self._o, xml, flags)
        if ret is None:raise libvirtError('virInterfaceDefineXML() failed', conn=self)
        __tmp = virInterface(self, _obj=ret)
        return __tmp

    def interfaceLookupByMACString(self, macstr):
        """Try to lookup an interface on the given hypervisor based on its MAC. """
        ret = libvirtmod.virInterfaceLookupByMACString(self._o, macstr)
        if ret is None:raise libvirtError('virInterfaceLookupByMACString() failed', conn=self)
        __tmp = virInterface(self, _obj=ret)
        return __tmp

    def interfaceLookupByName(self, name):
        """Try to lookup an interface on the given hypervisor based on its name. """
        ret = libvirtmod.virInterfaceLookupByName(self._o, name)
        if ret is None:raise libvirtError('virInterfaceLookupByName() failed', conn=self)
        __tmp = virInterface(self, _obj=ret)
        return __tmp

    def isAlive(self):
        """Determine if the connection to the hypervisor is still alive
        
        A connection will be classed as alive if it is either local, or running
        over a channel (TCP or UNIX socket) which is not closed. """
        ret = libvirtmod.virConnectIsAlive(self._o)
        if ret == -1: raise libvirtError ('virConnectIsAlive() failed', conn=self)
        return ret

    def isEncrypted(self):
        """Determine if the connection to the hypervisor is encrypted """
        ret = libvirtmod.virConnectIsEncrypted(self._o)
        if ret == -1: raise libvirtError ('virConnectIsEncrypted() failed', conn=self)
        return ret

    def isSecure(self):
        """Determine if the connection to the hypervisor is secure
        
        A connection will be classed as secure if it is either
        encrypted, or running over a channel which is not exposed
        to eavesdropping (eg a UNIX domain socket, or pipe) """
        ret = libvirtmod.virConnectIsSecure(self._o)
        if ret == -1: raise libvirtError ('virConnectIsSecure() failed', conn=self)
        return ret

    #
    # virConnect functions from module python
    #

    def listDefinedDomains(self):
        """list the defined domains, stores the pointers to the names in @names """
        ret = libvirtmod.virConnectListDefinedDomains(self._o)
        if ret is None: raise libvirtError ('virConnectListDefinedDomains() failed', conn=self)
        return ret

    def listDefinedInterfaces(self):
        """list the defined interfaces, stores the pointers to the names in @names """
        ret = libvirtmod.virConnectListDefinedInterfaces(self._o)
        if ret is None: raise libvirtError ('virConnectListDefinedInterfaces() failed', conn=self)
        return ret

    def listDefinedNetworks(self):
        """list the defined networks, stores the pointers to the names in @names """
        ret = libvirtmod.virConnectListDefinedNetworks(self._o)
        if ret is None: raise libvirtError ('virConnectListDefinedNetworks() failed', conn=self)
        return ret

    def listDefinedStoragePools(self):
        """list the defined storage pool, stores the pointers to the names in @names """
        ret = libvirtmod.virConnectListDefinedStoragePools(self._o)
        if ret is None: raise libvirtError ('virConnectListDefinedStoragePools() failed', conn=self)
        return ret

    def listDevices(self, cap, flags=0):
        """list the node devices """
        ret = libvirtmod.virNodeListDevices(self._o, cap, flags)
        if ret is None: raise libvirtError ('virNodeListDevices() failed', conn=self)
        return ret

    def listDomainsID(self):
        """Returns the list of the ID of the domains on the hypervisor """
        ret = libvirtmod.virConnectListDomainsID(self._o)
        if ret is None: raise libvirtError ('virConnectListDomainsID() failed', conn=self)
        return ret

    def listInterfaces(self):
        """list the running interfaces, stores the pointers to the names in @names """
        ret = libvirtmod.virConnectListInterfaces(self._o)
        if ret is None: raise libvirtError ('virConnectListInterfaces() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def listNWFilters(self):
        """List the defined network filters """
        ret = libvirtmod.virConnectListNWFilters(self._o)
        if ret is None: raise libvirtError ('virConnectListNWFilters() failed', conn=self)
        return ret

    #
    # virConnect functions from module python
    #

    def listNetworks(self):
        """list the networks, stores the pointers to the names in @names """
        ret = libvirtmod.virConnectListNetworks(self._o)
        if ret is None: raise libvirtError ('virConnectListNetworks() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def listSecrets(self):
        """List the defined secret IDs """
        ret = libvirtmod.virConnectListSecrets(self._o)
        if ret is None: raise libvirtError ('virConnectListSecrets() failed', conn=self)
        return ret

    #
    # virConnect functions from module python
    #

    def listStoragePools(self):
        """list the storage pools, stores the pointers to the names in @names """
        ret = libvirtmod.virConnectListStoragePools(self._o)
        if ret is None: raise libvirtError ('virConnectListStoragePools() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def lookupByID(self, id):
        """Try to find a domain based on the hypervisor ID number
        Note that this won't work for inactive domains which have an ID of -1,
        in that case a lookup based on the Name or UUId need to be done instead. """
        ret = libvirtmod.virDomainLookupByID(self._o, id)
        if ret is None:raise libvirtError('virDomainLookupByID() failed', conn=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    def lookupByName(self, name):
        """Try to lookup a domain on the given hypervisor based on its name. """
        ret = libvirtmod.virDomainLookupByName(self._o, name)
        if ret is None:raise libvirtError('virDomainLookupByName() failed', conn=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    #
    # virConnect functions from module python
    #

    def lookupByUUID(self, uuid):
        """Try to lookup a domain on the given hypervisor based on its UUID. """
        ret = libvirtmod.virDomainLookupByUUID(self._o, uuid)
        if ret is None:raise libvirtError('virDomainLookupByUUID() failed', conn=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    #
    # virConnect functions from module libvirt
    #

    def lookupByUUIDString(self, uuidstr):
        """Try to lookup a domain on the given hypervisor based on its UUID. """
        ret = libvirtmod.virDomainLookupByUUIDString(self._o, uuidstr)
        if ret is None:raise libvirtError('virDomainLookupByUUIDString() failed', conn=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

    def networkCreateXML(self, xmlDesc):
        """Create and start a new virtual network, based on an XML description
        similar to the one returned by virNetworkGetXMLDesc() """
        ret = libvirtmod.virNetworkCreateXML(self._o, xmlDesc)
        if ret is None:raise libvirtError('virNetworkCreateXML() failed', conn=self)
        __tmp = virNetwork(self, _obj=ret)
        return __tmp

    def networkDefineXML(self, xml):
        """Define a network, but does not create it """
        ret = libvirtmod.virNetworkDefineXML(self._o, xml)
        if ret is None:raise libvirtError('virNetworkDefineXML() failed', conn=self)
        __tmp = virNetwork(self, _obj=ret)
        return __tmp

    def networkLookupByName(self, name):
        """Try to lookup a network on the given hypervisor based on its name. """
        ret = libvirtmod.virNetworkLookupByName(self._o, name)
        if ret is None:raise libvirtError('virNetworkLookupByName() failed', conn=self)
        __tmp = virNetwork(self, _obj=ret)
        return __tmp

    #
    # virConnect functions from module python
    #

    def networkLookupByUUID(self, uuid):
        """Try to lookup a network on the given hypervisor based on its UUID. """
        ret = libvirtmod.virNetworkLookupByUUID(self._o, uuid)
        if ret is None:raise libvirtError('virNetworkLookupByUUID() failed', conn=self)
        __tmp = virNetwork(self, _obj=ret)
        return __tmp

    #
    # virConnect functions from module libvirt
    #

    def networkLookupByUUIDString(self, uuidstr):
        """Try to lookup a network on the given hypervisor based on its UUID. """
        ret = libvirtmod.virNetworkLookupByUUIDString(self._o, uuidstr)
        if ret is None:raise libvirtError('virNetworkLookupByUUIDString() failed', conn=self)
        __tmp = virNetwork(self, _obj=ret)
        return __tmp

    def newStream(self, flags=0):
        """Creates a new stream object which can be used to perform
        streamed I/O with other public API function.
        
        When no longer needed, a stream object must be released
        with virStreamFree. If a data stream has been used,
        then the application must call virStreamFinish or
        virStreamAbort before free'ing to, in order to notify
        the driver of termination.
        
        If a non-blocking data stream is required passed
        VIR_STREAM_NONBLOCK for flags, otherwise pass 0. """
        ret = libvirtmod.virStreamNew(self._o, flags)
        if ret is None:raise libvirtError('virStreamNew() failed', conn=self)
        __tmp = virStream(self, _obj=ret)
        return __tmp

    def nodeDeviceCreateXML(self, xmlDesc, flags=0):
        """Create a new device on the VM host machine, for example, virtual
        HBAs created using vport_create. """
        ret = libvirtmod.virNodeDeviceCreateXML(self._o, xmlDesc, flags)
        if ret is None:raise libvirtError('virNodeDeviceCreateXML() failed', conn=self)
        __tmp = virNodeDevice(self, _obj=ret)
        return __tmp

    def nodeDeviceLookupByName(self, name):
        """Lookup a node device by its name. """
        ret = libvirtmod.virNodeDeviceLookupByName(self._o, name)
        if ret is None:raise libvirtError('virNodeDeviceLookupByName() failed', conn=self)
        __tmp = virNodeDevice(self, _obj=ret)
        return __tmp

    def nodeDeviceLookupSCSIHostByWWN(self, wwnn, wwpn, flags=0):
        """Lookup SCSI Host which is capable with 'fc_host' by its WWNN and WWPN. """
        ret = libvirtmod.virNodeDeviceLookupSCSIHostByWWN(self._o, wwnn, wwpn, flags)
        if ret is None:raise libvirtError('virNodeDeviceLookupSCSIHostByWWN() failed', conn=self)
        __tmp = virNodeDevice(self, _obj=ret)
        return __tmp

    def numOfDefinedDomains(self):
        """Provides the number of defined but inactive domains. """
        ret = libvirtmod.virConnectNumOfDefinedDomains(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfDefinedDomains() failed', conn=self)
        return ret

    def numOfDefinedInterfaces(self):
        """Provides the number of defined (inactive) interfaces on the physical host. """
        ret = libvirtmod.virConnectNumOfDefinedInterfaces(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfDefinedInterfaces() failed', conn=self)
        return ret

    def numOfDefinedNetworks(self):
        """Provides the number of inactive networks. """
        ret = libvirtmod.virConnectNumOfDefinedNetworks(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfDefinedNetworks() failed', conn=self)
        return ret

    def numOfDefinedStoragePools(self):
        """Provides the number of inactive storage pools """
        ret = libvirtmod.virConnectNumOfDefinedStoragePools(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfDefinedStoragePools() failed', conn=self)
        return ret

    def numOfDevices(self, cap, flags=0):
        """Provides the number of node devices.
        
        If the optional 'cap'  argument is non-None, then the count
        will be restricted to devices with the specified capability """
        ret = libvirtmod.virNodeNumOfDevices(self._o, cap, flags)
        if ret == -1: raise libvirtError ('virNodeNumOfDevices() failed', conn=self)
        return ret

    def numOfDomains(self):
        """Provides the number of active domains. """
        ret = libvirtmod.virConnectNumOfDomains(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfDomains() failed', conn=self)
        return ret

    def numOfInterfaces(self):
        """Provides the number of active interfaces on the physical host. """
        ret = libvirtmod.virConnectNumOfInterfaces(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfInterfaces() failed', conn=self)
        return ret

    def numOfNWFilters(self):
        """Provides the number of nwfilters. """
        ret = libvirtmod.virConnectNumOfNWFilters(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfNWFilters() failed', conn=self)
        return ret

    def numOfNetworks(self):
        """Provides the number of active networks. """
        ret = libvirtmod.virConnectNumOfNetworks(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfNetworks() failed', conn=self)
        return ret

    def numOfSecrets(self):
        """Fetch number of currently defined secrets. """
        ret = libvirtmod.virConnectNumOfSecrets(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfSecrets() failed', conn=self)
        return ret

    def numOfStoragePools(self):
        """Provides the number of active storage pools """
        ret = libvirtmod.virConnectNumOfStoragePools(self._o)
        if ret == -1: raise libvirtError ('virConnectNumOfStoragePools() failed', conn=self)
        return ret

    def nwfilterDefineXML(self, xmlDesc):
        """Define a new network filter, based on an XML description
        similar to the one returned by virNWFilterGetXMLDesc() """
        ret = libvirtmod.virNWFilterDefineXML(self._o, xmlDesc)
        if ret is None:raise libvirtError('virNWFilterDefineXML() failed', conn=self)
        __tmp = virNWFilter(self, _obj=ret)
        return __tmp

    def nwfilterLookupByName(self, name):
        """Try to lookup a network filter on the given hypervisor based on its name. """
        ret = libvirtmod.virNWFilterLookupByName(self._o, name)
        if ret is None:raise libvirtError('virNWFilterLookupByName() failed', conn=self)
        __tmp = virNWFilter(self, _obj=ret)
        return __tmp

    #
    # virConnect functions from module python
    #

    def nwfilterLookupByUUID(self, uuid):
        """Try to lookup a network filter on the given hypervisor based on its UUID. """
        ret = libvirtmod.virNWFilterLookupByUUID(self._o, uuid)
        if ret is None:raise libvirtError('virNWFilterLookupByUUID() failed', conn=self)
        __tmp = virNWFilter(self, _obj=ret)
        return __tmp

    #
    # virConnect functions from module libvirt
    #

    def nwfilterLookupByUUIDString(self, uuidstr):
        """Try to lookup an nwfilter on the given hypervisor based on its UUID. """
        ret = libvirtmod.virNWFilterLookupByUUIDString(self._o, uuidstr)
        if ret is None:raise libvirtError('virNWFilterLookupByUUIDString() failed', conn=self)
        __tmp = virNWFilter(self, _obj=ret)
        return __tmp

    def restore(self, frm):
        """This method will restore a domain saved to disk by virDomainSave().
        
        See virDomainRestoreFlags() for more control. """
        ret = libvirtmod.virDomainRestore(self._o, frm)
        if ret == -1: raise libvirtError ('virDomainRestore() failed', conn=self)
        return ret

    def restoreFlags(self, frm, dxml=None, flags=0):
        """This method will restore a domain saved to disk by virDomainSave().
        
        If the hypervisor supports it, @dxml can be used to alter
        host-specific portions of the domain XML that will be used when
        restoring an image.  For example, it is possible to alter the
        backing filename that is associated with a disk device, in order to
        prepare for file renaming done as part of backing up the disk
        device while the domain is stopped.
        
        If @flags includes VIR_DOMAIN_SAVE_BYPASS_CACHE, then libvirt will
        attempt to bypass the file system cache while restoring the file, or
        fail if it cannot do so for the given system; this can allow less
        pressure on file system cache, but also risks slowing restores from NFS.
        
        Normally, the saved state file will remember whether the domain was
        running or paused, and restore defaults to the same state.
        Specifying VIR_DOMAIN_SAVE_RUNNING or VIR_DOMAIN_SAVE_PAUSED in
        @flags will override the default read from the file.  These two
        flags are mutually exclusive. """
        ret = libvirtmod.virDomainRestoreFlags(self._o, frm, dxml, flags)
        if ret == -1: raise libvirtError ('virDomainRestoreFlags() failed', conn=self)
        return ret

    def saveImageDefineXML(self, file, dxml, flags=0):
        """This updates the definition of a domain stored in a saved state
        file.  @file must be a file created previously by virDomainSave()
        or virDomainSaveFlags().
        
        @dxml can be used to alter host-specific portions of the domain XML
        that will be used when restoring an image.  For example, it is
        possible to alter the backing filename that is associated with a
        disk device, to match renaming done as part of backing up the disk
        device while the domain is stopped.
        
        Normally, the saved state file will remember whether the domain was
        running or paused, and restore defaults to the same state.
        Specifying VIR_DOMAIN_SAVE_RUNNING or VIR_DOMAIN_SAVE_PAUSED in
        @flags will override the default saved into the file; omitting both
        leaves the file's default unchanged.  These two flags are mutually
        exclusive. """
        ret = libvirtmod.virDomainSaveImageDefineXML(self._o, file, dxml, flags)
        if ret == -1: raise libvirtError ('virDomainSaveImageDefineXML() failed', conn=self)
        return ret

    def saveImageGetXMLDesc(self, file, flags=0):
        """This method will extract the XML describing the domain at the time
        a saved state file was created.  @file must be a file created
        previously by virDomainSave() or virDomainSaveFlags().
        
        No security-sensitive data will be included unless @flags contains
        VIR_DOMAIN_XML_SECURE; this flag is rejected on read-only
        connections.  For this API, @flags should not contain either
        VIR_DOMAIN_XML_INACTIVE or VIR_DOMAIN_XML_UPDATE_CPU. """
        ret = libvirtmod.virDomainSaveImageGetXMLDesc(self._o, file, flags)
        if ret is None: raise libvirtError ('virDomainSaveImageGetXMLDesc() failed', conn=self)
        return ret

    def secretDefineXML(self, xml, flags=0):
        """If XML specifies a UUID, locates the specified secret and replaces all
        attributes of the secret specified by UUID by attributes specified in xml
        (any attributes not specified in xml are discarded).
        
        Otherwise, creates a new secret with an automatically chosen UUID, and
        initializes its attributes from xml. """
        ret = libvirtmod.virSecretDefineXML(self._o, xml, flags)
        if ret is None:raise libvirtError('virSecretDefineXML() failed', conn=self)
        __tmp = virSecret(self, _obj=ret)
        return __tmp

    #
    # virConnect functions from module python
    #

    def secretLookupByUUID(self, uuid):
        """Try to lookup a secret on the given hypervisor based on its UUID. """
        ret = libvirtmod.virSecretLookupByUUID(self._o, uuid)
        if ret is None:raise libvirtError('virSecretLookupByUUID() failed', conn=self)
        __tmp = virSecret(self, _obj=ret)
        return __tmp

    #
    # virConnect functions from module libvirt
    #

    def secretLookupByUUIDString(self, uuidstr):
        """Try to lookup a secret on the given hypervisor based on its UUID.
        Uses the printable string value to describe the UUID """
        ret = libvirtmod.virSecretLookupByUUIDString(self._o, uuidstr)
        if ret is None:raise libvirtError('virSecretLookupByUUIDString() failed', conn=self)
        __tmp = virSecret(self, _obj=ret)
        return __tmp

    def secretLookupByUsage(self, usageType, usageID):
        """Try to lookup a secret on the given hypervisor based on its usage
        The usageID is unique within the set of secrets sharing the
        same usageType value. """
        ret = libvirtmod.virSecretLookupByUsage(self._o, usageType, usageID)
        if ret is None:raise libvirtError('virSecretLookupByUsage() failed', conn=self)
        __tmp = virSecret(self, _obj=ret)
        return __tmp

    def setKeepAlive(self, interval, count):
        """Start sending keepalive messages after @interval seconds of inactivity and
        consider the connection to be broken when no response is received after
        @count keepalive messages sent in a row.  In other words, sending count + 1
        keepalive message results in closing the connection.  When @interval is
        <= 0, no keepalive messages will be sent.  When @count is 0, the connection
        will be automatically closed after @interval seconds of inactivity without
        sending any keepalive messages.
        
        Note: The client has to implement and run an event loop with
        virEventRegisterImpl() or virEventRegisterDefaultImpl() to be able to
        use keepalive messages.  Failure to do so may result in connections
        being closed unexpectedly.
        
        Note: This API function controls only keepalive messages sent by the client.
        If the server is configured to use keepalive you still need to run the event
        loop to respond to them, even if you disable keepalives by this function. """
        ret = libvirtmod.virConnectSetKeepAlive(self._o, interval, count)
        if ret == -1: raise libvirtError ('virConnectSetKeepAlive() failed', conn=self)
        return ret

    #
    # virConnect functions from module python
    #

    def setMemoryParameters(self, params, flags=0):
        """Change the node memory tunables """
        ret = libvirtmod.virNodeSetMemoryParameters(self._o, params, flags)
        if ret == -1: raise libvirtError ('virNodeSetMemoryParameters() failed', conn=self)
        return ret

    #
    # virConnect functions from module libvirt
    #

    def storagePoolCreateXML(self, xmlDesc, flags=0):
        """Create a new storage based on its XML description. The
        pool is not persistent, so its definition will disappear
        when it is destroyed, or if the host is restarted """
        ret = libvirtmod.virStoragePoolCreateXML(self._o, xmlDesc, flags)
        if ret is None:raise libvirtError('virStoragePoolCreateXML() failed', conn=self)
        __tmp = virStoragePool(self, _obj=ret)
        return __tmp

    def storagePoolDefineXML(self, xml, flags=0):
        """Define a new inactive storage pool based on its XML description. The
        pool is persistent, until explicitly undefined. """
        ret = libvirtmod.virStoragePoolDefineXML(self._o, xml, flags)
        if ret is None:raise libvirtError('virStoragePoolDefineXML() failed', conn=self)
        __tmp = virStoragePool(self, _obj=ret)
        return __tmp

    def storagePoolLookupByName(self, name):
        """Fetch a storage pool based on its unique name """
        ret = libvirtmod.virStoragePoolLookupByName(self._o, name)
        if ret is None:raise libvirtError('virStoragePoolLookupByName() failed', conn=self)
        __tmp = virStoragePool(self, _obj=ret)
        return __tmp

    def storagePoolLookupByUUID(self, uuid):
        """Fetch a storage pool based on its globally unique id """
        ret = libvirtmod.virStoragePoolLookupByUUID(self._o, uuid)
        if ret is None:raise libvirtError('virStoragePoolLookupByUUID() failed', conn=self)
        __tmp = virStoragePool(self, _obj=ret)
        return __tmp

    def storagePoolLookupByUUIDString(self, uuidstr):
        """Fetch a storage pool based on its globally unique id """
        ret = libvirtmod.virStoragePoolLookupByUUIDString(self._o, uuidstr)
        if ret is None:raise libvirtError('virStoragePoolLookupByUUIDString() failed', conn=self)
        __tmp = virStoragePool(self, _obj=ret)
        return __tmp

    def storageVolLookupByKey(self, key):
        """Fetch a pointer to a storage volume based on its
        globally unique key """
        ret = libvirtmod.virStorageVolLookupByKey(self._o, key)
        if ret is None:raise libvirtError('virStorageVolLookupByKey() failed', conn=self)
        __tmp = virStorageVol(self, _obj=ret)
        return __tmp

    def storageVolLookupByPath(self, path):
        """Fetch a pointer to a storage volume based on its
        locally (host) unique path """
        ret = libvirtmod.virStorageVolLookupByPath(self._o, path)
        if ret is None:raise libvirtError('virStorageVolLookupByPath() failed', conn=self)
        __tmp = virStorageVol(self, _obj=ret)
        return __tmp

    def suspendForDuration(self, target, duration, flags=0):
        """Attempt to suspend the node (host machine) for the given duration of
        time in the specified state (Suspend-to-RAM, Suspend-to-Disk or
        Hybrid-Suspend). Schedule the node's Real-Time-Clock interrupt to
        resume the node after the duration is complete. """
        ret = libvirtmod.virNodeSuspendForDuration(self._o, target, duration, flags)
        if ret == -1: raise libvirtError ('virNodeSuspendForDuration() failed', conn=self)
        return ret

    #
    # virConnect functions from module virterror
    #

    def virConnGetLastError(self):
        """Provide a pointer to the last error caught on that connection
        
        This method is not protected against access from multiple
        threads. In a multi-threaded application, always use the
        global virGetLastError() API which is backed by thread
        local storage.
        
        If the connection object was discovered to be invalid by
        an API call, then the error will be reported against the
        global error object.
        
        Since 0.6.0, all errors reported in the per-connection object
        are also duplicated in the global error object. As such an
        application can always use virGetLastError(). This method
        remains for backwards compatibility. """
        ret = libvirtmod.virConnGetLastError(self._o)
        return ret

    def virConnResetLastError(self):
        """The error object is kept in thread local storage, so separate
        threads can safely access this concurrently.
        
        Reset the last error caught on that connection """
        libvirtmod.virConnResetLastError(self._o)

    #
    # virConnect methods from virConnect.py (hand coded)
    #
    def __del__(self):
        try:
           for cb,opaque in self.domainEventCallbacks.items():
               del self.domainEventCallbacks[cb]
           del self.domainEventCallbacks
           libvirtmod.virConnectDomainEventDeregister(self._o, self)
        except AttributeError:
           pass

        if self._o is not None:
            libvirtmod.virConnectClose(self._o)
        self._o = None

    def domainEventDeregister(self, cb):
        """Removes a Domain Event Callback. De-registering for a
           domain callback will disable delivery of this event type """
        try:
            del self.domainEventCallbacks[cb]
            if len(self.domainEventCallbacks) == 0:
                del self.domainEventCallbacks
                ret = libvirtmod.virConnectDomainEventDeregister(self._o, self)
                if ret == -1: raise libvirtError ('virConnectDomainEventDeregister() failed', conn=self)
        except AttributeError:
            pass

    def domainEventRegister(self, cb, opaque):
        """Adds a Domain Event Callback. Registering for a domain
           callback will enable delivery of the events """
        try:
            self.domainEventCallbacks[cb] = opaque
        except AttributeError:
            self.domainEventCallbacks = {cb:opaque}
            ret = libvirtmod.virConnectDomainEventRegister(self._o, self)
            if ret == -1: raise libvirtError ('virConnectDomainEventRegister() failed', conn=self)

    def _dispatchDomainEventCallbacks(self, dom, event, detail):
        """Dispatches events to python user domain event callbacks
        """
        try:
            for cb,opaque in self.domainEventCallbacks.items():
                cb(self, virDomain(self, _obj=dom), event, detail, opaque)
            return 0
        except AttributeError:
            pass

    def _dispatchDomainEventLifecycleCallback(self, dom, event, detail, cbData):
        """Dispatches events to python user domain lifecycle event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), event, detail, opaque)
        return 0

    def _dispatchDomainEventGenericCallback(self, dom, cbData):
        """Dispatches events to python user domain generic event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), opaque)
        return 0

    def _dispatchDomainEventRTCChangeCallback(self, dom, offset, cbData):
        """Dispatches events to python user domain RTC change event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), offset ,opaque)
        return 0

    def _dispatchDomainEventWatchdogCallback(self, dom, action, cbData):
        """Dispatches events to python user domain watchdog event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), action, opaque)
        return 0

    def _dispatchDomainEventIOErrorCallback(self, dom, srcPath, devAlias,
                                            action, cbData):
        """Dispatches events to python user domain IO error event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), srcPath, devAlias, action, opaque)
        return 0

    def _dispatchDomainEventIOErrorReasonCallback(self, dom, srcPath,
                                                  devAlias, action, reason,
                                                  cbData):
        """Dispatches events to python user domain IO error event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), srcPath, devAlias, action,
           reason, opaque)
        return 0

    def _dispatchDomainEventGraphicsCallback(self, dom, phase, localAddr,
                                            remoteAddr, authScheme, subject,
                                            cbData):
        """Dispatches events to python user domain graphics event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), phase, localAddr, remoteAddr,
           authScheme, subject, opaque)
        return 0

    def _dispatchDomainEventBlockPullCallback(self, dom, path, type, status, cbData):
        """Dispatches events to python user domain blockJob event callbacks
        """
        try:
            cb = cbData["cb"]
            opaque = cbData["opaque"]

            cb(self, virDomain(self, _obj=dom), path, type, status, opaque)
            return 0
        except AttributeError:
            pass

    def _dispatchDomainEventDiskChangeCallback(self, dom, oldSrcPath, newSrcPath, devAlias, reason, cbData):
        """Dispatches event to python user domain diskChange event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), oldSrcPath, newSrcPath, devAlias, reason, opaque)
        return 0

    def _dispatchDomainEventTrayChangeCallback(self, dom, devAlias, reason, cbData):
        """Dispatches event to python user domain trayChange event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), devAlias, reason, opaque)
        return 0

    def _dispatchDomainEventPMWakeupCallback(self, dom, reason, cbData):
        """Dispatches event to python user domain pmwakeup event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), reason, opaque)
        return 0

    def _dispatchDomainEventPMSuspendCallback(self, dom, reason, cbData):
        """Dispatches event to python user domain pmsuspend event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), reason, opaque)
        return 0

    def _dispatchDomainEventBalloonChangeCallback(self, dom, actual, cbData):
        """Dispatches events to python user domain balloon change event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), actual, opaque)
        return 0

    def _dispatchDomainEventPMSuspendDiskCallback(self, dom, reason, cbData):
        """Dispatches event to python user domain pmsuspend-disk event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), reason, opaque)
        return 0

    def _dispatchDomainEventDeviceRemovedCallback(self, dom, devAlias, cbData):
        """Dispatches event to python user domain device removed event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virDomain(self, _obj=dom), devAlias, opaque)
        return 0

    def domainEventDeregisterAny(self, callbackID):
        """Removes a Domain Event Callback. De-registering for a
           domain callback will disable delivery of this event type """
        try:
            ret = libvirtmod.virConnectDomainEventDeregisterAny(self._o, callbackID)
            if ret == -1: raise libvirtError ('virConnectDomainEventDeregisterAny() failed', conn=self)
            del self.domainEventCallbackID[callbackID]
        except AttributeError:
            pass

    def _dispatchNetworkEventLifecycleCallback(self, net, event, detail, cbData):
        """Dispatches events to python user network lifecycle event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, virNetwork(self, _obj=net), event, detail, opaque)
        return 0

    def networkEventDeregisterAny(self, callbackID):
        """Removes a Network Event Callback. De-registering for a
           network callback will disable delivery of this event type"""
        try:
            ret = libvirtmod.virConnectNetworkEventDeregisterAny(self._o, callbackID)
            if ret == -1: raise libvirtError ('virConnectNetworkEventDeregisterAny() failed', conn=self)
            del self.networkEventCallbackID[callbackID]
        except AttributeError:
            pass

    def networkEventRegisterAny(self, net, eventID, cb, opaque):
        """Adds a Network Event Callback. Registering for a network
           callback will enable delivery of the events"""
        if not hasattr(self, 'networkEventCallbackID'):
            self.networkEventCallbackID = {}
        cbData = { "cb": cb, "conn": self, "opaque": opaque }
        if net is None:
            ret = libvirtmod.virConnectNetworkEventRegisterAny(self._o, None, eventID, cbData)
        else:
            ret = libvirtmod.virConnectNetworkEventRegisterAny(self._o, net._o, eventID, cbData)
        if ret == -1:
            raise libvirtError ('virConnectNetworkEventRegisterAny() failed', conn=self)
        self.networkEventCallbackID[ret] = opaque
        return ret

    def domainEventRegisterAny(self, dom, eventID, cb, opaque):
        """Adds a Domain Event Callback. Registering for a domain
           callback will enable delivery of the events """
        if not hasattr(self, 'domainEventCallbackID'):
            self.domainEventCallbackID = {}
        cbData = { "cb": cb, "conn": self, "opaque": opaque }
        if dom is None:
            ret = libvirtmod.virConnectDomainEventRegisterAny(self._o, None, eventID, cbData)
        else:
            ret = libvirtmod.virConnectDomainEventRegisterAny(self._o, dom._o, eventID, cbData)
        if ret == -1:
            raise libvirtError ('virConnectDomainEventRegisterAny() failed', conn=self)
        self.domainEventCallbackID[ret] = opaque
        return ret

    def listAllDomains(self, flags=0):
        """List all domains and returns a list of domain objects"""
        ret = libvirtmod.virConnectListAllDomains(self._o, flags)
        if ret is None:
            raise libvirtError("virConnectListAllDomains() failed", conn=self)

        retlist = list()
        for domptr in ret:
            retlist.append(virDomain(self, _obj=domptr))

        return retlist

    def listAllStoragePools(self, flags=0):
        """Returns a list of storage pool objects"""
        ret = libvirtmod.virConnectListAllStoragePools(self._o, flags)
        if ret is None:
            raise libvirtError("virConnectListAllStoragePools() failed", conn=self)

        retlist = list()
        for poolptr in ret:
            retlist.append(virStoragePool(self, _obj=poolptr))

        return retlist

    def listAllNetworks(self, flags=0):
        """Returns a list of network objects"""
        ret = libvirtmod.virConnectListAllNetworks(self._o, flags)
        if ret is None:
            raise libvirtError("virConnectListAllNetworks() failed", conn=self)

        retlist = list()
        for netptr in ret:
            retlist.append(virNetwork(self, _obj=netptr))

        return retlist

    def listAllInterfaces(self, flags=0):
        """Returns a list of interface objects"""
        ret = libvirtmod.virConnectListAllInterfaces(self._o, flags)
        if ret is None:
            raise libvirtError("virConnectListAllInterfaces() failed", conn=self)

        retlist = list()
        for ifaceptr in ret:
            retlist.append(virInterface(self, _obj=ifaceptr))

        return retlist

    def listAllDevices(self, flags=0):
        """Returns a list of host node device objects"""
        ret = libvirtmod.virConnectListAllNodeDevices(self._o, flags)
        if ret is None:
            raise libvirtError("virConnectListAllNodeDevices() failed", conn=self)

        retlist = list()
        for devptr in ret:
            retlist.append(virNodeDevice(self, _obj=devptr))

        return retlist

    def listAllNWFilters(self, flags=0):
        """Returns a list of network filter objects"""
        ret = libvirtmod.virConnectListAllNWFilters(self._o, flags)
        if ret is None:
            raise libvirtError("virConnectListAllNWFilters() failed", conn=self)

        retlist = list()
        for filter_ptr in ret:
            retlist.append(virNWFilter(self, _obj=filter_ptr))

        return retlist

    def listAllSecrets(self, flags=0):
        """Returns a list of secret objects"""
        ret = libvirtmod.virConnectListAllSecrets(self._o, flags)
        if ret is None:
            raise libvirtError("virConnectListAllSecrets() failed", conn=self)

        retlist = list()
        for secret_ptr in ret:
            retlist.append(virSecret(self, _obj=secret_ptr))

        return retlist

    def _dispatchCloseCallback(self, reason, cbData):
        """Dispatches events to python user close callback"""
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, reason, opaque)
        return 0


    def unregisterCloseCallback(self):
        """Removes a close event callback"""
        ret = libvirtmod.virConnectUnregisterCloseCallback(self._o)
        if ret == -1: raise libvirtError ('virConnectUnregisterCloseCallback() failed', conn=self)

    def registerCloseCallback(self, cb, opaque):
        """Adds a close event callback, providing a notification
         when a connection fails / closes"""
        cbData = { "cb": cb, "conn": self, "opaque": opaque }
        ret = libvirtmod.virConnectRegisterCloseCallback(self._o, cbData)
        if ret == -1:
            raise libvirtError ('virConnectRegisterCloseCallback() failed', conn=self)
        return ret

    def createXMLWithFiles(self, xmlDesc, files, flags=0):
        """Launch a new guest domain, based on an XML description similar
        to the one returned by virDomainGetXMLDesc()
        This function may require privileged access to the hypervisor.
        The domain is not persistent, so its definition will disappear when it
        is destroyed, or if the host is restarted (see virDomainDefineXML() to
        define persistent domains).

        @files provides an array of file descriptors which will be
        made available to the 'init' process of the guest. The file
        handles exposed to the guest will be renumbered to start
        from 3 (ie immediately following stderr). This is only
        supported for guests which use container based virtualization
        technology.

        If the VIR_DOMAIN_START_PAUSED flag is set, the guest domain
        will be started, but its CPUs will remain paused. The CPUs
        can later be manually started using virDomainResume.

        If the VIR_DOMAIN_START_AUTODESTROY flag is set, the guest
        domain will be automatically destroyed when the virConnectPtr
        object is finally released. This will also happen if the
        client application crashes / loses its connection to the
        libvirtd daemon. Any domains marked for auto destroy will
        block attempts at migration, save-to-file, or snapshots. """
        ret = libvirtmod.virDomainCreateXMLWithFiles(self._o, xmlDesc, files, flags)
        if ret is None:raise libvirtError('virDomainCreateXMLWithFiles() failed', conn=self)
        __tmp = virDomain(self,_obj=ret)
        return __tmp

class virNodeDevice(object):
    def __init__(self, conn, _obj=None):
        self._conn = conn
        self._o = _obj

    def __del__(self):
        if self._o is not None:
            libvirtmod.virNodeDeviceFree(self._o)
        self._o = None

    def connect(self):
        return self._conn

    #
    # virNodeDevice functions from module libvirt
    #

    def XMLDesc(self, flags=0):
        """Fetch an XML document describing all aspects of
        the device. """
        ret = libvirtmod.virNodeDeviceGetXMLDesc(self._o, flags)
        if ret is None: raise libvirtError ('virNodeDeviceGetXMLDesc() failed')
        return ret

    def destroy(self):
        """Destroy the device object. The virtual device (only works for vHBA
        currently) is removed from the host operating system.  This function
        may require privileged access. """
        ret = libvirtmod.virNodeDeviceDestroy(self._o)
        if ret == -1: raise libvirtError ('virNodeDeviceDestroy() failed')
        return ret

    def detachFlags(self, driverName, flags=0):
        """Detach the node device from the node itself so that it may be
        assigned to a guest domain.
        
        Depending on the hypervisor, this may involve operations such as
        unbinding any device drivers from the device, binding the device to
        a dummy device driver and resetting the device. Different backend
        drivers expect the device to be bound to different dummy
        devices. For example, QEMU's "kvm" backend driver (the default)
        expects the device to be bound to "pci-stub", but its "vfio"
        backend driver expects the device to be bound to "vfio-pci".
        
        If the device is currently in use by the node, this method may
        fail.
        
        Once the device is not assigned to any guest, it may be re-attached
        to the node using the virNodeDeviceReAttach() method. """
        ret = libvirtmod.virNodeDeviceDetachFlags(self._o, driverName, flags)
        if ret == -1: raise libvirtError ('virNodeDeviceDetachFlags() failed')
        return ret

    def dettach(self):
        """Dettach the node device from the node itself so that it may be
        assigned to a guest domain.
        
        Depending on the hypervisor, this may involve operations such
        as unbinding any device drivers from the device, binding the
        device to a dummy device driver and resetting the device.
        
        If the device is currently in use by the node, this method may
        fail.
        
        Once the device is not assigned to any guest, it may be re-attached
        to the node using the virNodeDeviceReattach() method.
        
        If the caller needs control over which backend driver will be used
        during PCI device assignment (to use something other than the
        default, for example VFIO), the newer virNodeDeviceDetachFlags()
        API should be used instead. """
        ret = libvirtmod.virNodeDeviceDettach(self._o)
        if ret == -1: raise libvirtError ('virNodeDeviceDettach() failed')
        return ret

    #
    # virNodeDevice functions from module python
    #

    def listCaps(self):
        """list the node device's capabilities """
        ret = libvirtmod.virNodeDeviceListCaps(self._o)
        if ret is None: raise libvirtError ('virNodeDeviceListCaps() failed')
        return ret

    #
    # virNodeDevice functions from module libvirt
    #

    def name(self):
        """Just return the device name """
        ret = libvirtmod.virNodeDeviceGetName(self._o)
        return ret

    def numOfCaps(self):
        """Accessor for the number of capabilities supported by the device. """
        ret = libvirtmod.virNodeDeviceNumOfCaps(self._o)
        if ret == -1: raise libvirtError ('virNodeDeviceNumOfCaps() failed')
        return ret

    def parent(self):
        """Accessor for the parent of the device """
        ret = libvirtmod.virNodeDeviceGetParent(self._o)
        return ret

    def reAttach(self):
        """Re-attach a previously dettached node device to the node so that it
        may be used by the node again.
        
        Depending on the hypervisor, this may involve operations such
        as resetting the device, unbinding it from a dummy device driver
        and binding it to its appropriate driver.
        
        If the device is currently in use by a guest, this method may fail. """
        ret = libvirtmod.virNodeDeviceReAttach(self._o)
        if ret == -1: raise libvirtError ('virNodeDeviceReAttach() failed')
        return ret

    def reset(self):
        """Reset a previously dettached node device to the node before or
        after assigning it to a guest.
        
        The exact reset semantics depends on the hypervisor and device
        type but, for example, KVM will attempt to reset PCI devices with
        a Function Level Reset, Secondary Bus Reset or a Power Management
        D-State reset.
        
        If the reset will affect other devices which are currently in use,
        this function may fail. """
        ret = libvirtmod.virNodeDeviceReset(self._o)
        if ret == -1: raise libvirtError ('virNodeDeviceReset() failed')
        return ret

class virSecret(object):
    def __init__(self, conn, _obj=None):
        self._conn = conn
        self._o = _obj

    def __del__(self):
        if self._o is not None:
            libvirtmod.virSecretFree(self._o)
        self._o = None

    def connect(self):
        return self._conn

    #
    # virSecret functions from module python
    #

    def UUID(self):
        """Extract the UUID unique Identifier of a secret. """
        ret = libvirtmod.virSecretGetUUID(self._o)
        if ret is None: raise libvirtError ('virSecretGetUUID() failed')
        return ret

    def UUIDString(self):
        """Fetch globally unique ID of the secret as a string. """
        ret = libvirtmod.virSecretGetUUIDString(self._o)
        if ret is None: raise libvirtError ('virSecretGetUUIDString() failed')
        return ret

    #
    # virSecret functions from module libvirt
    #

    def XMLDesc(self, flags=0):
        """Fetches an XML document describing attributes of the secret. """
        ret = libvirtmod.virSecretGetXMLDesc(self._o, flags)
        if ret is None: raise libvirtError ('virSecretGetXMLDesc() failed')
        return ret

    def setValue(self, value, flags=0):
        """Associates a value with a secret. """
        ret = libvirtmod.virSecretSetValue(self._o, value, flags)
        if ret == -1: raise libvirtError ('virSecretSetValue() failed')
        return ret

    def undefine(self):
        """Deletes the specified secret.  This does not free the associated
        virSecretPtr object. """
        ret = libvirtmod.virSecretUndefine(self._o)
        if ret == -1: raise libvirtError ('virSecretUndefine() failed')
        return ret

    def usageID(self):
        """Get the unique identifier of the object with which this
        secret is to be used. The format of the identifier is
        dependant on the usage type of the secret. For a secret
        with a usage type of VIR_SECRET_USAGE_TYPE_VOLUME the
        identifier will be a fully qualfied path name. The
        identifiers are intended to be unique within the set of
        all secrets sharing the same usage type. ie, there shall
        only ever be one secret for each volume path. """
        ret = libvirtmod.virSecretGetUsageID(self._o)
        return ret

    def usageType(self):
        """Get the type of object which uses this secret. The returned
        value is one of the constants defined in the virSecretUsageType
        enumeration. More values may be added to this enumeration in
        the future, so callers should expect to see usage types they
        do not explicitly know about. """
        ret = libvirtmod.virSecretGetUsageType(self._o)
        return ret

    def value(self, flags=0):
        """Fetches the value associated with a secret. """
        ret = libvirtmod.virSecretGetValue(self._o, flags)
        if ret is None: raise libvirtError ('virSecretGetValue() failed')
        return ret

class virNWFilter(object):
    def __init__(self, conn, _obj=None):
        self._conn = conn
        self._o = _obj

    def __del__(self):
        if self._o is not None:
            libvirtmod.virNWFilterFree(self._o)
        self._o = None

    def connect(self):
        return self._conn

    #
    # virNWFilter functions from module python
    #

    def UUID(self):
        """Extract the UUID unique Identifier of a network filter. """
        ret = libvirtmod.virNWFilterGetUUID(self._o)
        if ret is None: raise libvirtError ('virNWFilterGetUUID() failed')
        return ret

    def UUIDString(self):
        """Fetch globally unique ID of the network filter as a string. """
        ret = libvirtmod.virNWFilterGetUUIDString(self._o)
        if ret is None: raise libvirtError ('virNWFilterGetUUIDString() failed')
        return ret

    #
    # virNWFilter functions from module libvirt
    #

    def XMLDesc(self, flags=0):
        """Provide an XML description of the network filter. The description may be
        reused later to redefine the network filter with virNWFilterCreateXML(). """
        ret = libvirtmod.virNWFilterGetXMLDesc(self._o, flags)
        if ret is None: raise libvirtError ('virNWFilterGetXMLDesc() failed')
        return ret

    def name(self):
        """Get the public name for the network filter """
        ret = libvirtmod.virNWFilterGetName(self._o)
        return ret

    def undefine(self):
        """Undefine the nwfilter object. This call will not succeed if
        a running VM is referencing the filter. This does not free the
        associated virNWFilterPtr object. """
        ret = libvirtmod.virNWFilterUndefine(self._o)
        if ret == -1: raise libvirtError ('virNWFilterUndefine() failed')
        return ret

class virStream(object):
    def __init__(self, conn, _obj=None):
        self._conn = conn
        self._o = _obj

    def connect(self):
        return self._conn

    #
    # virStream functions from module libvirt
    #

    def abort(self):
        """Request that the in progress data transfer be cancelled
        abnormally before the end of the stream has been reached.
        For output streams this can be used to inform the driver
        that the stream is being terminated early. For input
        streams this can be used to inform the driver that it
        should stop sending data. """
        ret = libvirtmod.virStreamAbort(self._o)
        if ret == -1: raise libvirtError ('virStreamAbort() failed')
        return ret

    def eventRemoveCallback(self):
        """Remove an event callback from the stream """
        ret = libvirtmod.virStreamEventRemoveCallback(self._o)
        if ret == -1: raise libvirtError ('virStreamEventRemoveCallback() failed')
        return ret

    def eventUpdateCallback(self, events):
        """Changes the set of events to monitor for a stream. This allows
        for event notification to be changed without having to
        unregister & register the callback completely. This method
        is guaranteed to succeed if a callback is already registered """
        ret = libvirtmod.virStreamEventUpdateCallback(self._o, events)
        if ret == -1: raise libvirtError ('virStreamEventUpdateCallback() failed')
        return ret

    def finish(self):
        """Indicate that there is no further data is to be transmitted
        on the stream. For output streams this should be called once
        all data has been written. For input streams this should be
        called once virStreamRecv returns end-of-file.
        
        This method is a synchronization point for all asynchronous
        errors, so if this returns a success code the application can
        be sure that all data has been successfully processed. """
        ret = libvirtmod.virStreamFinish(self._o)
        if ret == -1: raise libvirtError ('virStreamFinish() failed')
        return ret

    #
    # virStream methods from virStream.py (hand coded)
    #
    def __del__(self):
        try:
            if self.cb:
                libvirtmod.virStreamEventRemoveCallback(self._o)
        except AttributeError:
           pass

        if self._o is not None:
            libvirtmod.virStreamFree(self._o)
        self._o = None

    def _dispatchStreamEventCallback(self, events, cbData):
        """
        Dispatches events to python user's stream event callbacks
        """
        cb = cbData["cb"]
        opaque = cbData["opaque"]

        cb(self, events, opaque)
        return 0

    def eventAddCallback(self, events, cb, opaque):
        self.cb = cb
        cbData = {"stream": self, "cb" : cb, "opaque" : opaque}
        ret = libvirtmod.virStreamEventAddCallback(self._o, events, cbData)
        if ret == -1: raise libvirtError ('virStreamEventAddCallback() failed')

    def recvAll(self, handler, opaque):
        """Receive the entire data stream, sending the data to the
        requested data sink. This is simply a convenient alternative
        to virStreamRecv, for apps that do blocking-I/O.

        A hypothetical handler function looks like:

            def handler(stream, # virStream instance
                        buf,    # string containing received data
                        opaque): # extra data passed to recvAll as opaque
                fd = opaque
                return os.write(fd, buf)
        """
        while True:
            got = self.recv(1024*64)
            if got == -2:
                raise libvirtError("cannot use recvAll with "
                                   "nonblocking stream")
            if len(got) == 0:
                break

            try:
                ret = handler(self, got, opaque)
                if type(ret) is int and ret < 0:
                    raise RuntimeError("recvAll handler returned %d" % ret)
            except Exception:
                e = sys.exc_info()[1]
                try:
                    self.abort()
                except:
                    pass
                raise e

    def sendAll(self, handler, opaque):
        """
        Send the entire data stream, reading the data from the
        requested data source. This is simply a convenient alternative
        to virStreamSend, for apps that do blocking-I/O.

        A hypothetical handler function looks like:

            def handler(stream, # virStream instance
                        nbytes, # int amt of data to read
                        opaque): # extra data passed to recvAll as opaque
                fd = opaque
                return os.read(fd, nbytes)
        """
        while True:
            try:
                got = handler(self, 1024*64, opaque)
            except:
                e = sys.exc_info()[1]
                try:
                    self.abort()
                except:
                    pass
                raise e

            if got == "":
                break

            ret = self.send(got)
            if ret == -2:
                raise libvirtError("cannot use sendAll with "
                                   "nonblocking stream")

    def recv(self, nbytes):
        """Reads a series of bytes from the stream. This method may
        block the calling application for an arbitrary amount
        of time.

        Errors are not guaranteed to be reported synchronously
        with the call, but may instead be delayed until a
        subsequent call.

        On success, the received data is returned. On failure, an
        exception is raised. If the stream is a NONBLOCK stream and
        the request would block, integer -2 is returned.
        """
        ret = libvirtmod.virStreamRecv(self._o, nbytes)
        if ret is None: raise libvirtError ('virStreamRecv() failed')
        return ret

    def send(self, data):
        """Write a series of bytes to the stream. This method may
        block the calling application for an arbitrary amount
        of time. Once an application has finished sending data
        it should call virStreamFinish to wait for successful
        confirmation from the driver, or detect any error

        This method may not be used if a stream source has been
        registered

        Errors are not guaranteed to be reported synchronously
        with the call, but may instead be delayed until a
        subsequent call.
        """
        ret = libvirtmod.virStreamSend(self._o, data)
        if ret == -1: raise libvirtError ('virStreamSend() failed')
        return ret

class virDomainSnapshot(object):
    def __init__(self, dom, _obj=None):
        self._dom = dom
        self._conn = dom.connect()
        self._o = _obj

    def __del__(self):
        if self._o is not None:
            libvirtmod.virDomainSnapshotFree(self._o)
        self._o = None

    def connect(self):
        return self._conn

    def domain(self):
        return self._dom

    #
    # virDomainSnapshot functions from module libvirt
    #

    def delete(self, flags=0):
        """Delete the snapshot.
        
        If @flags is 0, then just this snapshot is deleted, and changes
        from this snapshot are automatically merged into children
        snapshots.  If @flags includes VIR_DOMAIN_SNAPSHOT_DELETE_CHILDREN,
        then this snapshot and any descendant snapshots are deleted.  If
        @flags includes VIR_DOMAIN_SNAPSHOT_DELETE_CHILDREN_ONLY, then any
        descendant snapshots are deleted, but this snapshot remains.  These
        two flags are mutually exclusive.
        
        If @flags includes VIR_DOMAIN_SNAPSHOT_DELETE_METADATA_ONLY, then
        any snapshot metadata tracked by libvirt is removed while keeping
        the snapshot contents intact; if a hypervisor does not require any
        libvirt metadata to track snapshots, then this flag is silently
        ignored. """
        ret = libvirtmod.virDomainSnapshotDelete(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainSnapshotDelete() failed')
        return ret

    def getName(self):
        """Get the public name for that snapshot """
        ret = libvirtmod.virDomainSnapshotGetName(self._o)
        if ret is None: raise libvirtError ('virDomainSnapshotGetName() failed')
        return ret

    def getParent(self, flags=0):
        """Get the parent snapshot for @snapshot, if any. """
        ret = libvirtmod.virDomainSnapshotGetParent(self._o, flags)
        if ret is None:raise libvirtError('virDomainSnapshotGetParent() failed', dom=self._dom)
        __tmp = virDomainSnapshot(self,_obj=ret)
        return __tmp

    def getXMLDesc(self, flags=0):
        """Provide an XML description of the domain snapshot.
        
        No security-sensitive data will be included unless @flags contains
        VIR_DOMAIN_XML_SECURE; this flag is rejected on read-only
        connections.  For this API, @flags should not contain either
        VIR_DOMAIN_XML_INACTIVE or VIR_DOMAIN_XML_UPDATE_CPU. """
        ret = libvirtmod.virDomainSnapshotGetXMLDesc(self._o, flags)
        if ret is None: raise libvirtError ('virDomainSnapshotGetXMLDesc() failed')
        return ret

    def hasMetadata(self, flags=0):
        """Determine if the given snapshot is associated with libvirt metadata
        that would prevent the deletion of the domain. """
        ret = libvirtmod.virDomainSnapshotHasMetadata(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainSnapshotHasMetadata() failed')
        return ret

    def isCurrent(self, flags=0):
        """Determine if the given snapshot is the domain's current snapshot.  See
        also virDomainHasCurrentSnapshot(). """
        ret = libvirtmod.virDomainSnapshotIsCurrent(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainSnapshotIsCurrent() failed')
        return ret

    #
    # virDomainSnapshot functions from module python
    #

    def listChildrenNames(self, flags=0):
        """collect the list of child snapshot names for the given snapshot """
        ret = libvirtmod.virDomainSnapshotListChildrenNames(self._o, flags)
        if ret is None: raise libvirtError ('virDomainSnapshotListChildrenNames() failed')
        return ret

    #
    # virDomainSnapshot functions from module libvirt
    #

    def numChildren(self, flags=0):
        """Provides the number of child snapshots for this domain snapshot.
        
        By default, this command covers only direct children; it is also possible
        to expand things to cover all descendants, when @flags includes
        VIR_DOMAIN_SNAPSHOT_LIST_DESCENDANTS.  Also, some filters are provided in
        groups, where each group contains bits that describe mutually exclusive
        attributes of a snapshot, and where all bits within a group describe
        all possible snapshots.  Some hypervisors might reject explicit bits
        from a group where the hypervisor cannot make a distinction.  For a
        group supported by a given hypervisor, the behavior when no bits of a
        group are set is identical to the behavior when all bits in that group
        are set.  When setting bits from more than one group, it is possible to
        select an impossible combination, in that case a hypervisor may return
        either 0 or an error.
        
        The first group of @flags is VIR_DOMAIN_SNAPSHOT_LIST_LEAVES and
        VIR_DOMAIN_SNAPSHOT_LIST_NO_LEAVES, to filter based on snapshots that
        have no further children (a leaf snapshot).
        
        The next group of @flags is VIR_DOMAIN_SNAPSHOT_LIST_METADATA and
        VIR_DOMAIN_SNAPSHOT_LIST_NO_METADATA, for filtering snapshots based on
        whether they have metadata that would prevent the removal of the last
        reference to a domain.
        
        The next group of @flags is VIR_DOMAIN_SNAPSHOT_LIST_INACTIVE,
        VIR_DOMAIN_SNAPSHOT_LIST_ACTIVE, and VIR_DOMAIN_SNAPSHOT_LIST_DISK_ONLY,
        for filtering snapshots based on what domain state is tracked by the
        snapshot.
        
        The next group of @flags is VIR_DOMAIN_SNAPSHOT_LIST_INTERNAL and
        VIR_DOMAIN_SNAPSHOT_LIST_EXTERNAL, for filtering snapshots based on
        whether the snapshot is stored inside the disk images or as
        additional files. """
        ret = libvirtmod.virDomainSnapshotNumChildren(self._o, flags)
        if ret == -1: raise libvirtError ('virDomainSnapshotNumChildren() failed')
        return ret

    #
    # virDomainSnapshot methods from virDomainSnapshot.py (hand coded)
    #
    def getConnect(self):
        """Get the connection that owns the domain that a snapshot was created for"""
        return self.connect()

    def getDomain(self):
        """Get the domain that a snapshot was created for"""
        return self.domain()

    def listAllChildren(self, flags=0):
        """List all child snapshots and returns a list of snapshot objects"""
        ret = libvirtmod.virDomainSnapshotListAllChildren(self._o, flags)
        if ret is None:
            raise libvirtError("virDomainSnapshotListAllChildren() failed", conn=self)

        retlist = list()
        for snapptr in ret:
            retlist.append(virDomainSnapshot(self, _obj=snapptr))

        return retlist

# virBlkioParameterType
VIR_DOMAIN_BLKIO_PARAM_INT = 1
VIR_DOMAIN_BLKIO_PARAM_UINT = 2
VIR_DOMAIN_BLKIO_PARAM_LLONG = 3
VIR_DOMAIN_BLKIO_PARAM_ULLONG = 4
VIR_DOMAIN_BLKIO_PARAM_DOUBLE = 5
VIR_DOMAIN_BLKIO_PARAM_BOOLEAN = 6

# virCPUCompareResult
VIR_CPU_COMPARE_ERROR = -1
VIR_CPU_COMPARE_INCOMPATIBLE = 0
VIR_CPU_COMPARE_IDENTICAL = 1
VIR_CPU_COMPARE_SUPERSET = 2

# virConnectBaselineCPUFlags
VIR_CONNECT_BASELINE_CPU_EXPAND_FEATURES = 1

# virConnectCloseReason
VIR_CONNECT_CLOSE_REASON_ERROR = 0
VIR_CONNECT_CLOSE_REASON_EOF = 1
VIR_CONNECT_CLOSE_REASON_KEEPALIVE = 2
VIR_CONNECT_CLOSE_REASON_CLIENT = 3

# virConnectCredentialType
VIR_CRED_USERNAME = 1
VIR_CRED_AUTHNAME = 2
VIR_CRED_LANGUAGE = 3
VIR_CRED_CNONCE = 4
VIR_CRED_PASSPHRASE = 5
VIR_CRED_ECHOPROMPT = 6
VIR_CRED_NOECHOPROMPT = 7
VIR_CRED_REALM = 8
VIR_CRED_EXTERNAL = 9

# virConnectDomainEventBlockJobStatus
VIR_DOMAIN_BLOCK_JOB_COMPLETED = 0
VIR_DOMAIN_BLOCK_JOB_FAILED = 1
VIR_DOMAIN_BLOCK_JOB_CANCELED = 2
VIR_DOMAIN_BLOCK_JOB_READY = 3

# virConnectDomainEventDiskChangeReason
VIR_DOMAIN_EVENT_DISK_CHANGE_MISSING_ON_START = 0
VIR_DOMAIN_EVENT_DISK_DROP_MISSING_ON_START = 1

# virConnectFlags
VIR_CONNECT_RO = 1
VIR_CONNECT_NO_ALIASES = 2

# virConnectListAllDomainsFlags
VIR_CONNECT_LIST_DOMAINS_ACTIVE = 1
VIR_CONNECT_LIST_DOMAINS_INACTIVE = 2
VIR_CONNECT_LIST_DOMAINS_PERSISTENT = 4
VIR_CONNECT_LIST_DOMAINS_TRANSIENT = 8
VIR_CONNECT_LIST_DOMAINS_RUNNING = 16
VIR_CONNECT_LIST_DOMAINS_PAUSED = 32
VIR_CONNECT_LIST_DOMAINS_SHUTOFF = 64
VIR_CONNECT_LIST_DOMAINS_OTHER = 128
VIR_CONNECT_LIST_DOMAINS_MANAGEDSAVE = 256
VIR_CONNECT_LIST_DOMAINS_NO_MANAGEDSAVE = 512
VIR_CONNECT_LIST_DOMAINS_AUTOSTART = 1024
VIR_CONNECT_LIST_DOMAINS_NO_AUTOSTART = 2048
VIR_CONNECT_LIST_DOMAINS_HAS_SNAPSHOT = 4096
VIR_CONNECT_LIST_DOMAINS_NO_SNAPSHOT = 8192

# virConnectListAllInterfacesFlags
VIR_CONNECT_LIST_INTERFACES_INACTIVE = 1
VIR_CONNECT_LIST_INTERFACES_ACTIVE = 2

# virConnectListAllNetworksFlags
VIR_CONNECT_LIST_NETWORKS_INACTIVE = 1
VIR_CONNECT_LIST_NETWORKS_ACTIVE = 2
VIR_CONNECT_LIST_NETWORKS_PERSISTENT = 4
VIR_CONNECT_LIST_NETWORKS_TRANSIENT = 8
VIR_CONNECT_LIST_NETWORKS_AUTOSTART = 16
VIR_CONNECT_LIST_NETWORKS_NO_AUTOSTART = 32

# virConnectListAllNodeDeviceFlags
VIR_CONNECT_LIST_NODE_DEVICES_CAP_SYSTEM = 1
VIR_CONNECT_LIST_NODE_DEVICES_CAP_PCI_DEV = 2
VIR_CONNECT_LIST_NODE_DEVICES_CAP_USB_DEV = 4
VIR_CONNECT_LIST_NODE_DEVICES_CAP_USB_INTERFACE = 8
VIR_CONNECT_LIST_NODE_DEVICES_CAP_NET = 16
VIR_CONNECT_LIST_NODE_DEVICES_CAP_SCSI_HOST = 32
VIR_CONNECT_LIST_NODE_DEVICES_CAP_SCSI_TARGET = 64
VIR_CONNECT_LIST_NODE_DEVICES_CAP_SCSI = 128
VIR_CONNECT_LIST_NODE_DEVICES_CAP_STORAGE = 256
VIR_CONNECT_LIST_NODE_DEVICES_CAP_FC_HOST = 512
VIR_CONNECT_LIST_NODE_DEVICES_CAP_VPORTS = 1024
VIR_CONNECT_LIST_NODE_DEVICES_CAP_SCSI_GENERIC = 2048

# virConnectListAllSecretsFlags
VIR_CONNECT_LIST_SECRETS_EPHEMERAL = 1
VIR_CONNECT_LIST_SECRETS_NO_EPHEMERAL = 2
VIR_CONNECT_LIST_SECRETS_PRIVATE = 4
VIR_CONNECT_LIST_SECRETS_NO_PRIVATE = 8

# virConnectListAllStoragePoolsFlags
VIR_CONNECT_LIST_STORAGE_POOLS_INACTIVE = 1
VIR_CONNECT_LIST_STORAGE_POOLS_ACTIVE = 2
VIR_CONNECT_LIST_STORAGE_POOLS_PERSISTENT = 4
VIR_CONNECT_LIST_STORAGE_POOLS_TRANSIENT = 8
VIR_CONNECT_LIST_STORAGE_POOLS_AUTOSTART = 16
VIR_CONNECT_LIST_STORAGE_POOLS_NO_AUTOSTART = 32
VIR_CONNECT_LIST_STORAGE_POOLS_DIR = 64
VIR_CONNECT_LIST_STORAGE_POOLS_FS = 128
VIR_CONNECT_LIST_STORAGE_POOLS_NETFS = 256
VIR_CONNECT_LIST_STORAGE_POOLS_LOGICAL = 512
VIR_CONNECT_LIST_STORAGE_POOLS_DISK = 1024
VIR_CONNECT_LIST_STORAGE_POOLS_ISCSI = 2048
VIR_CONNECT_LIST_STORAGE_POOLS_SCSI = 4096
VIR_CONNECT_LIST_STORAGE_POOLS_MPATH = 8192
VIR_CONNECT_LIST_STORAGE_POOLS_RBD = 16384
VIR_CONNECT_LIST_STORAGE_POOLS_SHEEPDOG = 32768
VIR_CONNECT_LIST_STORAGE_POOLS_GLUSTER = 65536

# virDomainBlockCommitFlags
VIR_DOMAIN_BLOCK_COMMIT_SHALLOW = 1
VIR_DOMAIN_BLOCK_COMMIT_DELETE = 2

# virDomainBlockJobAbortFlags
VIR_DOMAIN_BLOCK_JOB_ABORT_ASYNC = 1
VIR_DOMAIN_BLOCK_JOB_ABORT_PIVOT = 2

# virDomainBlockJobType
VIR_DOMAIN_BLOCK_JOB_TYPE_UNKNOWN = 0
VIR_DOMAIN_BLOCK_JOB_TYPE_PULL = 1
VIR_DOMAIN_BLOCK_JOB_TYPE_COPY = 2
VIR_DOMAIN_BLOCK_JOB_TYPE_COMMIT = 3

# virDomainBlockRebaseFlags
VIR_DOMAIN_BLOCK_REBASE_SHALLOW = 1
VIR_DOMAIN_BLOCK_REBASE_REUSE_EXT = 2
VIR_DOMAIN_BLOCK_REBASE_COPY_RAW = 4
VIR_DOMAIN_BLOCK_REBASE_COPY = 8

# virDomainBlockResizeFlags
VIR_DOMAIN_BLOCK_RESIZE_BYTES = 1

# virDomainBlockedReason
VIR_DOMAIN_BLOCKED_UNKNOWN = 0

# virDomainChannelFlags
VIR_DOMAIN_CHANNEL_FORCE = 1

# virDomainConsoleFlags
VIR_DOMAIN_CONSOLE_FORCE = 1
VIR_DOMAIN_CONSOLE_SAFE = 2

# virDomainControlState
VIR_DOMAIN_CONTROL_OK = 0
VIR_DOMAIN_CONTROL_JOB = 1
VIR_DOMAIN_CONTROL_OCCUPIED = 2
VIR_DOMAIN_CONTROL_ERROR = 3

# virDomainCoreDumpFlags
VIR_DUMP_CRASH = 1
VIR_DUMP_LIVE = 2
VIR_DUMP_BYPASS_CACHE = 4
VIR_DUMP_RESET = 8
VIR_DUMP_MEMORY_ONLY = 16

# virDomainCrashedReason
VIR_DOMAIN_CRASHED_UNKNOWN = 0
VIR_DOMAIN_CRASHED_PANICKED = 1

# virDomainCreateFlags
VIR_DOMAIN_NONE = 0
VIR_DOMAIN_START_PAUSED = 1
VIR_DOMAIN_START_AUTODESTROY = 2
VIR_DOMAIN_START_BYPASS_CACHE = 4
VIR_DOMAIN_START_FORCE_BOOT = 8

# virDomainDestroyFlagsValues
VIR_DOMAIN_DESTROY_DEFAULT = 0
VIR_DOMAIN_DESTROY_GRACEFUL = 1

# virDomainDeviceModifyFlags
VIR_DOMAIN_DEVICE_MODIFY_CURRENT = 0
VIR_DOMAIN_DEVICE_MODIFY_LIVE = 1
VIR_DOMAIN_DEVICE_MODIFY_CONFIG = 2
VIR_DOMAIN_DEVICE_MODIFY_FORCE = 4

# virDomainDiskErrorCode
VIR_DOMAIN_DISK_ERROR_NONE = 0
VIR_DOMAIN_DISK_ERROR_UNSPEC = 1
VIR_DOMAIN_DISK_ERROR_NO_SPACE = 2

# virDomainEventCrashedDetailType
VIR_DOMAIN_EVENT_CRASHED_PANICKED = 0

# virDomainEventDefinedDetailType
VIR_DOMAIN_EVENT_DEFINED_ADDED = 0
VIR_DOMAIN_EVENT_DEFINED_UPDATED = 1

# virDomainEventGraphicsAddressType
VIR_DOMAIN_EVENT_GRAPHICS_ADDRESS_IPV4 = 1
VIR_DOMAIN_EVENT_GRAPHICS_ADDRESS_IPV6 = 2
VIR_DOMAIN_EVENT_GRAPHICS_ADDRESS_UNIX = 3

# virDomainEventGraphicsPhase
VIR_DOMAIN_EVENT_GRAPHICS_CONNECT = 0
VIR_DOMAIN_EVENT_GRAPHICS_INITIALIZE = 1
VIR_DOMAIN_EVENT_GRAPHICS_DISCONNECT = 2

# virDomainEventID
VIR_DOMAIN_EVENT_ID_LIFECYCLE = 0
VIR_DOMAIN_EVENT_ID_REBOOT = 1
VIR_DOMAIN_EVENT_ID_RTC_CHANGE = 2
VIR_DOMAIN_EVENT_ID_WATCHDOG = 3
VIR_DOMAIN_EVENT_ID_IO_ERROR = 4
VIR_DOMAIN_EVENT_ID_GRAPHICS = 5
VIR_DOMAIN_EVENT_ID_IO_ERROR_REASON = 6
VIR_DOMAIN_EVENT_ID_CONTROL_ERROR = 7
VIR_DOMAIN_EVENT_ID_BLOCK_JOB = 8
VIR_DOMAIN_EVENT_ID_DISK_CHANGE = 9
VIR_DOMAIN_EVENT_ID_TRAY_CHANGE = 10
VIR_DOMAIN_EVENT_ID_PMWAKEUP = 11
VIR_DOMAIN_EVENT_ID_PMSUSPEND = 12
VIR_DOMAIN_EVENT_ID_BALLOON_CHANGE = 13
VIR_DOMAIN_EVENT_ID_PMSUSPEND_DISK = 14
VIR_DOMAIN_EVENT_ID_DEVICE_REMOVED = 15

# virDomainEventIOErrorAction
VIR_DOMAIN_EVENT_IO_ERROR_NONE = 0
VIR_DOMAIN_EVENT_IO_ERROR_PAUSE = 1
VIR_DOMAIN_EVENT_IO_ERROR_REPORT = 2

# virDomainEventPMSuspendedDetailType
VIR_DOMAIN_EVENT_PMSUSPENDED_MEMORY = 0
VIR_DOMAIN_EVENT_PMSUSPENDED_DISK = 1

# virDomainEventResumedDetailType
VIR_DOMAIN_EVENT_RESUMED_UNPAUSED = 0
VIR_DOMAIN_EVENT_RESUMED_MIGRATED = 1
VIR_DOMAIN_EVENT_RESUMED_FROM_SNAPSHOT = 2

# virDomainEventShutdownDetailType
VIR_DOMAIN_EVENT_SHUTDOWN_FINISHED = 0

# virDomainEventStartedDetailType
VIR_DOMAIN_EVENT_STARTED_BOOTED = 0
VIR_DOMAIN_EVENT_STARTED_MIGRATED = 1
VIR_DOMAIN_EVENT_STARTED_RESTORED = 2
VIR_DOMAIN_EVENT_STARTED_FROM_SNAPSHOT = 3
VIR_DOMAIN_EVENT_STARTED_WAKEUP = 4

# virDomainEventStoppedDetailType
VIR_DOMAIN_EVENT_STOPPED_SHUTDOWN = 0
VIR_DOMAIN_EVENT_STOPPED_DESTROYED = 1
VIR_DOMAIN_EVENT_STOPPED_CRASHED = 2
VIR_DOMAIN_EVENT_STOPPED_MIGRATED = 3
VIR_DOMAIN_EVENT_STOPPED_SAVED = 4
VIR_DOMAIN_EVENT_STOPPED_FAILED = 5
VIR_DOMAIN_EVENT_STOPPED_FROM_SNAPSHOT = 6

# virDomainEventSuspendedDetailType
VIR_DOMAIN_EVENT_SUSPENDED_PAUSED = 0
VIR_DOMAIN_EVENT_SUSPENDED_MIGRATED = 1
VIR_DOMAIN_EVENT_SUSPENDED_IOERROR = 2
VIR_DOMAIN_EVENT_SUSPENDED_WATCHDOG = 3
VIR_DOMAIN_EVENT_SUSPENDED_RESTORED = 4
VIR_DOMAIN_EVENT_SUSPENDED_FROM_SNAPSHOT = 5
VIR_DOMAIN_EVENT_SUSPENDED_API_ERROR = 6

# virDomainEventTrayChangeReason
VIR_DOMAIN_EVENT_TRAY_CHANGE_OPEN = 0
VIR_DOMAIN_EVENT_TRAY_CHANGE_CLOSE = 1

# virDomainEventType
VIR_DOMAIN_EVENT_DEFINED = 0
VIR_DOMAIN_EVENT_UNDEFINED = 1
VIR_DOMAIN_EVENT_STARTED = 2
VIR_DOMAIN_EVENT_SUSPENDED = 3
VIR_DOMAIN_EVENT_RESUMED = 4
VIR_DOMAIN_EVENT_STOPPED = 5
VIR_DOMAIN_EVENT_SHUTDOWN = 6
VIR_DOMAIN_EVENT_PMSUSPENDED = 7
VIR_DOMAIN_EVENT_CRASHED = 8

# virDomainEventUndefinedDetailType
VIR_DOMAIN_EVENT_UNDEFINED_REMOVED = 0

# virDomainEventWatchdogAction
VIR_DOMAIN_EVENT_WATCHDOG_NONE = 0
VIR_DOMAIN_EVENT_WATCHDOG_PAUSE = 1
VIR_DOMAIN_EVENT_WATCHDOG_RESET = 2
VIR_DOMAIN_EVENT_WATCHDOG_POWEROFF = 3
VIR_DOMAIN_EVENT_WATCHDOG_SHUTDOWN = 4
VIR_DOMAIN_EVENT_WATCHDOG_DEBUG = 5

# virDomainJobType
VIR_DOMAIN_JOB_NONE = 0
VIR_DOMAIN_JOB_BOUNDED = 1
VIR_DOMAIN_JOB_UNBOUNDED = 2
VIR_DOMAIN_JOB_COMPLETED = 3
VIR_DOMAIN_JOB_FAILED = 4
VIR_DOMAIN_JOB_CANCELLED = 5

# virDomainMemoryFlags
VIR_MEMORY_VIRTUAL = 1
VIR_MEMORY_PHYSICAL = 2

# virDomainMemoryModFlags
VIR_DOMAIN_MEM_CURRENT = 0
VIR_DOMAIN_MEM_LIVE = 1
VIR_DOMAIN_MEM_CONFIG = 2
VIR_DOMAIN_MEM_MAXIMUM = 4

# virDomainMemoryStatTags
VIR_DOMAIN_MEMORY_STAT_SWAP_IN = 0
VIR_DOMAIN_MEMORY_STAT_SWAP_OUT = 1
VIR_DOMAIN_MEMORY_STAT_MAJOR_FAULT = 2
VIR_DOMAIN_MEMORY_STAT_MINOR_FAULT = 3
VIR_DOMAIN_MEMORY_STAT_UNUSED = 4
VIR_DOMAIN_MEMORY_STAT_AVAILABLE = 5
VIR_DOMAIN_MEMORY_STAT_ACTUAL_BALLOON = 6
VIR_DOMAIN_MEMORY_STAT_RSS = 7
VIR_DOMAIN_MEMORY_STAT_NR = 8

# virDomainMetadataType
VIR_DOMAIN_METADATA_DESCRIPTION = 0
VIR_DOMAIN_METADATA_TITLE = 1
VIR_DOMAIN_METADATA_ELEMENT = 2

# virDomainMigrateFlags
VIR_MIGRATE_LIVE = 1
VIR_MIGRATE_PEER2PEER = 2
VIR_MIGRATE_TUNNELLED = 4
VIR_MIGRATE_PERSIST_DEST = 8
VIR_MIGRATE_UNDEFINE_SOURCE = 16
VIR_MIGRATE_PAUSED = 32
VIR_MIGRATE_NON_SHARED_DISK = 64
VIR_MIGRATE_NON_SHARED_INC = 128
VIR_MIGRATE_CHANGE_PROTECTION = 256
VIR_MIGRATE_UNSAFE = 512
VIR_MIGRATE_OFFLINE = 1024
VIR_MIGRATE_COMPRESSED = 2048
VIR_MIGRATE_ABORT_ON_ERROR = 4096

# virDomainModificationImpact
VIR_DOMAIN_AFFECT_CURRENT = 0
VIR_DOMAIN_AFFECT_LIVE = 1
VIR_DOMAIN_AFFECT_CONFIG = 2

# virDomainNostateReason
VIR_DOMAIN_NOSTATE_UNKNOWN = 0

# virDomainNumatuneMemMode
VIR_DOMAIN_NUMATUNE_MEM_STRICT = 0
VIR_DOMAIN_NUMATUNE_MEM_PREFERRED = 1
VIR_DOMAIN_NUMATUNE_MEM_INTERLEAVE = 2

# virDomainOpenGraphicsFlags
VIR_DOMAIN_OPEN_GRAPHICS_SKIPAUTH = 1

# virDomainPMSuspendedDiskReason
VIR_DOMAIN_PMSUSPENDED_DISK_UNKNOWN = 0

# virDomainPMSuspendedReason
VIR_DOMAIN_PMSUSPENDED_UNKNOWN = 0

# virDomainPausedReason
VIR_DOMAIN_PAUSED_UNKNOWN = 0
VIR_DOMAIN_PAUSED_USER = 1
VIR_DOMAIN_PAUSED_MIGRATION = 2
VIR_DOMAIN_PAUSED_SAVE = 3
VIR_DOMAIN_PAUSED_DUMP = 4
VIR_DOMAIN_PAUSED_IOERROR = 5
VIR_DOMAIN_PAUSED_WATCHDOG = 6
VIR_DOMAIN_PAUSED_FROM_SNAPSHOT = 7
VIR_DOMAIN_PAUSED_SHUTTING_DOWN = 8
VIR_DOMAIN_PAUSED_SNAPSHOT = 9
VIR_DOMAIN_PAUSED_CRASHED = 10

# virDomainProcessSignal
VIR_DOMAIN_PROCESS_SIGNAL_NOP = 0
VIR_DOMAIN_PROCESS_SIGNAL_HUP = 1
VIR_DOMAIN_PROCESS_SIGNAL_INT = 2
VIR_DOMAIN_PROCESS_SIGNAL_QUIT = 3
VIR_DOMAIN_PROCESS_SIGNAL_ILL = 4
VIR_DOMAIN_PROCESS_SIGNAL_TRAP = 5
VIR_DOMAIN_PROCESS_SIGNAL_ABRT = 6
VIR_DOMAIN_PROCESS_SIGNAL_BUS = 7
VIR_DOMAIN_PROCESS_SIGNAL_FPE = 8
VIR_DOMAIN_PROCESS_SIGNAL_KILL = 9
VIR_DOMAIN_PROCESS_SIGNAL_USR1 = 10
VIR_DOMAIN_PROCESS_SIGNAL_SEGV = 11
VIR_DOMAIN_PROCESS_SIGNAL_USR2 = 12
VIR_DOMAIN_PROCESS_SIGNAL_PIPE = 13
VIR_DOMAIN_PROCESS_SIGNAL_ALRM = 14
VIR_DOMAIN_PROCESS_SIGNAL_TERM = 15
VIR_DOMAIN_PROCESS_SIGNAL_STKFLT = 16
VIR_DOMAIN_PROCESS_SIGNAL_CHLD = 17
VIR_DOMAIN_PROCESS_SIGNAL_CONT = 18
VIR_DOMAIN_PROCESS_SIGNAL_STOP = 19
VIR_DOMAIN_PROCESS_SIGNAL_TSTP = 20
VIR_DOMAIN_PROCESS_SIGNAL_TTIN = 21
VIR_DOMAIN_PROCESS_SIGNAL_TTOU = 22
VIR_DOMAIN_PROCESS_SIGNAL_URG = 23
VIR_DOMAIN_PROCESS_SIGNAL_XCPU = 24
VIR_DOMAIN_PROCESS_SIGNAL_XFSZ = 25
VIR_DOMAIN_PROCESS_SIGNAL_VTALRM = 26
VIR_DOMAIN_PROCESS_SIGNAL_PROF = 27
VIR_DOMAIN_PROCESS_SIGNAL_WINCH = 28
VIR_DOMAIN_PROCESS_SIGNAL_POLL = 29
VIR_DOMAIN_PROCESS_SIGNAL_PWR = 30
VIR_DOMAIN_PROCESS_SIGNAL_SYS = 31
VIR_DOMAIN_PROCESS_SIGNAL_RT0 = 32
VIR_DOMAIN_PROCESS_SIGNAL_RT1 = 33
VIR_DOMAIN_PROCESS_SIGNAL_RT2 = 34
VIR_DOMAIN_PROCESS_SIGNAL_RT3 = 35
VIR_DOMAIN_PROCESS_SIGNAL_RT4 = 36
VIR_DOMAIN_PROCESS_SIGNAL_RT5 = 37
VIR_DOMAIN_PROCESS_SIGNAL_RT6 = 38
VIR_DOMAIN_PROCESS_SIGNAL_RT7 = 39
VIR_DOMAIN_PROCESS_SIGNAL_RT8 = 40
VIR_DOMAIN_PROCESS_SIGNAL_RT9 = 41
VIR_DOMAIN_PROCESS_SIGNAL_RT10 = 42
VIR_DOMAIN_PROCESS_SIGNAL_RT11 = 43
VIR_DOMAIN_PROCESS_SIGNAL_RT12 = 44
VIR_DOMAIN_PROCESS_SIGNAL_RT13 = 45
VIR_DOMAIN_PROCESS_SIGNAL_RT14 = 46
VIR_DOMAIN_PROCESS_SIGNAL_RT15 = 47
VIR_DOMAIN_PROCESS_SIGNAL_RT16 = 48
VIR_DOMAIN_PROCESS_SIGNAL_RT17 = 49
VIR_DOMAIN_PROCESS_SIGNAL_RT18 = 50
VIR_DOMAIN_PROCESS_SIGNAL_RT19 = 51
VIR_DOMAIN_PROCESS_SIGNAL_RT20 = 52
VIR_DOMAIN_PROCESS_SIGNAL_RT21 = 53
VIR_DOMAIN_PROCESS_SIGNAL_RT22 = 54
VIR_DOMAIN_PROCESS_SIGNAL_RT23 = 55
VIR_DOMAIN_PROCESS_SIGNAL_RT24 = 56
VIR_DOMAIN_PROCESS_SIGNAL_RT25 = 57
VIR_DOMAIN_PROCESS_SIGNAL_RT26 = 58
VIR_DOMAIN_PROCESS_SIGNAL_RT27 = 59
VIR_DOMAIN_PROCESS_SIGNAL_RT28 = 60
VIR_DOMAIN_PROCESS_SIGNAL_RT29 = 61
VIR_DOMAIN_PROCESS_SIGNAL_RT30 = 62
VIR_DOMAIN_PROCESS_SIGNAL_RT31 = 63
VIR_DOMAIN_PROCESS_SIGNAL_RT32 = 64

# virDomainRebootFlagValues
VIR_DOMAIN_REBOOT_DEFAULT = 0
VIR_DOMAIN_REBOOT_ACPI_POWER_BTN = 1
VIR_DOMAIN_REBOOT_GUEST_AGENT = 2
VIR_DOMAIN_REBOOT_INITCTL = 4
VIR_DOMAIN_REBOOT_SIGNAL = 8

# virDomainRunningReason
VIR_DOMAIN_RUNNING_UNKNOWN = 0
VIR_DOMAIN_RUNNING_BOOTED = 1
VIR_DOMAIN_RUNNING_MIGRATED = 2
VIR_DOMAIN_RUNNING_RESTORED = 3
VIR_DOMAIN_RUNNING_FROM_SNAPSHOT = 4
VIR_DOMAIN_RUNNING_UNPAUSED = 5
VIR_DOMAIN_RUNNING_MIGRATION_CANCELED = 6
VIR_DOMAIN_RUNNING_SAVE_CANCELED = 7
VIR_DOMAIN_RUNNING_WAKEUP = 8
VIR_DOMAIN_RUNNING_CRASHED = 9

# virDomainSaveRestoreFlags
VIR_DOMAIN_SAVE_BYPASS_CACHE = 1
VIR_DOMAIN_SAVE_RUNNING = 2
VIR_DOMAIN_SAVE_PAUSED = 4

# virDomainShutdownFlagValues
VIR_DOMAIN_SHUTDOWN_DEFAULT = 0
VIR_DOMAIN_SHUTDOWN_ACPI_POWER_BTN = 1
VIR_DOMAIN_SHUTDOWN_GUEST_AGENT = 2
VIR_DOMAIN_SHUTDOWN_INITCTL = 4
VIR_DOMAIN_SHUTDOWN_SIGNAL = 8

# virDomainShutdownReason
VIR_DOMAIN_SHUTDOWN_UNKNOWN = 0
VIR_DOMAIN_SHUTDOWN_USER = 1

# virDomainShutoffReason
VIR_DOMAIN_SHUTOFF_UNKNOWN = 0
VIR_DOMAIN_SHUTOFF_SHUTDOWN = 1
VIR_DOMAIN_SHUTOFF_DESTROYED = 2
VIR_DOMAIN_SHUTOFF_CRASHED = 3
VIR_DOMAIN_SHUTOFF_MIGRATED = 4
VIR_DOMAIN_SHUTOFF_SAVED = 5
VIR_DOMAIN_SHUTOFF_FAILED = 6
VIR_DOMAIN_SHUTOFF_FROM_SNAPSHOT = 7

# virDomainSnapshotCreateFlags
VIR_DOMAIN_SNAPSHOT_CREATE_REDEFINE = 1
VIR_DOMAIN_SNAPSHOT_CREATE_CURRENT = 2
VIR_DOMAIN_SNAPSHOT_CREATE_NO_METADATA = 4
VIR_DOMAIN_SNAPSHOT_CREATE_HALT = 8
VIR_DOMAIN_SNAPSHOT_CREATE_DISK_ONLY = 16
VIR_DOMAIN_SNAPSHOT_CREATE_REUSE_EXT = 32
VIR_DOMAIN_SNAPSHOT_CREATE_QUIESCE = 64
VIR_DOMAIN_SNAPSHOT_CREATE_ATOMIC = 128
VIR_DOMAIN_SNAPSHOT_CREATE_LIVE = 256

# virDomainSnapshotDeleteFlags
VIR_DOMAIN_SNAPSHOT_DELETE_CHILDREN = 1
VIR_DOMAIN_SNAPSHOT_DELETE_METADATA_ONLY = 2
VIR_DOMAIN_SNAPSHOT_DELETE_CHILDREN_ONLY = 4

# virDomainSnapshotListFlags
VIR_DOMAIN_SNAPSHOT_LIST_ROOTS = 1
VIR_DOMAIN_SNAPSHOT_LIST_DESCENDANTS = 1
VIR_DOMAIN_SNAPSHOT_LIST_METADATA = 2
VIR_DOMAIN_SNAPSHOT_LIST_LEAVES = 4
VIR_DOMAIN_SNAPSHOT_LIST_NO_LEAVES = 8
VIR_DOMAIN_SNAPSHOT_LIST_NO_METADATA = 16
VIR_DOMAIN_SNAPSHOT_LIST_INACTIVE = 32
VIR_DOMAIN_SNAPSHOT_LIST_ACTIVE = 64
VIR_DOMAIN_SNAPSHOT_LIST_DISK_ONLY = 128
VIR_DOMAIN_SNAPSHOT_LIST_INTERNAL = 256
VIR_DOMAIN_SNAPSHOT_LIST_EXTERNAL = 512

# virDomainSnapshotRevertFlags
VIR_DOMAIN_SNAPSHOT_REVERT_RUNNING = 1
VIR_DOMAIN_SNAPSHOT_REVERT_PAUSED = 2
VIR_DOMAIN_SNAPSHOT_REVERT_FORCE = 4

# virDomainState
VIR_DOMAIN_NOSTATE = 0
VIR_DOMAIN_RUNNING = 1
VIR_DOMAIN_BLOCKED = 2
VIR_DOMAIN_PAUSED = 3
VIR_DOMAIN_SHUTDOWN = 4
VIR_DOMAIN_SHUTOFF = 5
VIR_DOMAIN_CRASHED = 6
VIR_DOMAIN_PMSUSPENDED = 7

# virDomainUndefineFlagsValues
VIR_DOMAIN_UNDEFINE_MANAGED_SAVE = 1
VIR_DOMAIN_UNDEFINE_SNAPSHOTS_METADATA = 2

# virDomainVcpuFlags
VIR_DOMAIN_VCPU_CURRENT = 0
VIR_DOMAIN_VCPU_LIVE = 1
VIR_DOMAIN_VCPU_CONFIG = 2
VIR_DOMAIN_VCPU_MAXIMUM = 4
VIR_DOMAIN_VCPU_GUEST = 8

# virDomainXMLFlags
VIR_DOMAIN_XML_SECURE = 1
VIR_DOMAIN_XML_INACTIVE = 2
VIR_DOMAIN_XML_UPDATE_CPU = 4
VIR_DOMAIN_XML_MIGRATABLE = 8

# virErrorDomain
VIR_FROM_NONE = 0
VIR_FROM_XEN = 1
VIR_FROM_XEND = 2
VIR_FROM_XENSTORE = 3
VIR_FROM_SEXPR = 4
VIR_FROM_XML = 5
VIR_FROM_DOM = 6
VIR_FROM_RPC = 7
VIR_FROM_PROXY = 8
VIR_FROM_CONF = 9
VIR_FROM_QEMU = 10
VIR_FROM_NET = 11
VIR_FROM_TEST = 12
VIR_FROM_REMOTE = 13
VIR_FROM_OPENVZ = 14
VIR_FROM_XENXM = 15
VIR_FROM_STATS_LINUX = 16
VIR_FROM_LXC = 17
VIR_FROM_STORAGE = 18
VIR_FROM_NETWORK = 19
VIR_FROM_DOMAIN = 20
VIR_FROM_UML = 21
VIR_FROM_NODEDEV = 22
VIR_FROM_XEN_INOTIFY = 23
VIR_FROM_SECURITY = 24
VIR_FROM_VBOX = 25
VIR_FROM_INTERFACE = 26
VIR_FROM_ONE = 27
VIR_FROM_ESX = 28
VIR_FROM_PHYP = 29
VIR_FROM_SECRET = 30
VIR_FROM_CPU = 31
VIR_FROM_XENAPI = 32
VIR_FROM_NWFILTER = 33
VIR_FROM_HOOK = 34
VIR_FROM_DOMAIN_SNAPSHOT = 35
VIR_FROM_AUDIT = 36
VIR_FROM_SYSINFO = 37
VIR_FROM_STREAMS = 38
VIR_FROM_VMWARE = 39
VIR_FROM_EVENT = 40
VIR_FROM_LIBXL = 41
VIR_FROM_LOCKING = 42
VIR_FROM_HYPERV = 43
VIR_FROM_CAPABILITIES = 44
VIR_FROM_URI = 45
VIR_FROM_AUTH = 46
VIR_FROM_DBUS = 47
VIR_FROM_PARALLELS = 48
VIR_FROM_DEVICE = 49
VIR_FROM_SSH = 50
VIR_FROM_LOCKSPACE = 51
VIR_FROM_INITCTL = 52
VIR_FROM_IDENTITY = 53
VIR_FROM_CGROUP = 54
VIR_FROM_ACCESS = 55
VIR_FROM_SYSTEMD = 56

# virErrorLevel
VIR_ERR_NONE = 0
VIR_ERR_WARNING = 1
VIR_ERR_ERROR = 2

# virErrorNumber
VIR_ERR_OK = 0
VIR_ERR_INTERNAL_ERROR = 1
VIR_ERR_NO_MEMORY = 2
VIR_ERR_NO_SUPPORT = 3
VIR_ERR_UNKNOWN_HOST = 4
VIR_ERR_NO_CONNECT = 5
VIR_ERR_INVALID_CONN = 6
VIR_ERR_INVALID_DOMAIN = 7
VIR_ERR_INVALID_ARG = 8
VIR_ERR_OPERATION_FAILED = 9
VIR_ERR_GET_FAILED = 10
VIR_ERR_POST_FAILED = 11
VIR_ERR_HTTP_ERROR = 12
VIR_ERR_SEXPR_SERIAL = 13
VIR_ERR_NO_XEN = 14
VIR_ERR_XEN_CALL = 15
VIR_ERR_OS_TYPE = 16
VIR_ERR_NO_KERNEL = 17
VIR_ERR_NO_ROOT = 18
VIR_ERR_NO_SOURCE = 19
VIR_ERR_NO_TARGET = 20
VIR_ERR_NO_NAME = 21
VIR_ERR_NO_OS = 22
VIR_ERR_NO_DEVICE = 23
VIR_ERR_NO_XENSTORE = 24
VIR_ERR_DRIVER_FULL = 25
VIR_ERR_CALL_FAILED = 26
VIR_ERR_XML_ERROR = 27
VIR_ERR_DOM_EXIST = 28
VIR_ERR_OPERATION_DENIED = 29
VIR_ERR_OPEN_FAILED = 30
VIR_ERR_READ_FAILED = 31
VIR_ERR_PARSE_FAILED = 32
VIR_ERR_CONF_SYNTAX = 33
VIR_ERR_WRITE_FAILED = 34
VIR_ERR_XML_DETAIL = 35
VIR_ERR_INVALID_NETWORK = 36
VIR_ERR_NETWORK_EXIST = 37
VIR_ERR_SYSTEM_ERROR = 38
VIR_ERR_RPC = 39
VIR_ERR_GNUTLS_ERROR = 40
VIR_WAR_NO_NETWORK = 41
VIR_ERR_NO_DOMAIN = 42
VIR_ERR_NO_NETWORK = 43
VIR_ERR_INVALID_MAC = 44
VIR_ERR_AUTH_FAILED = 45
VIR_ERR_INVALID_STORAGE_POOL = 46
VIR_ERR_INVALID_STORAGE_VOL = 47
VIR_WAR_NO_STORAGE = 48
VIR_ERR_NO_STORAGE_POOL = 49
VIR_ERR_NO_STORAGE_VOL = 50
VIR_WAR_NO_NODE = 51
VIR_ERR_INVALID_NODE_DEVICE = 52
VIR_ERR_NO_NODE_DEVICE = 53
VIR_ERR_NO_SECURITY_MODEL = 54
VIR_ERR_OPERATION_INVALID = 55
VIR_WAR_NO_INTERFACE = 56
VIR_ERR_NO_INTERFACE = 57
VIR_ERR_INVALID_INTERFACE = 58
VIR_ERR_MULTIPLE_INTERFACES = 59
VIR_WAR_NO_NWFILTER = 60
VIR_ERR_INVALID_NWFILTER = 61
VIR_ERR_NO_NWFILTER = 62
VIR_ERR_BUILD_FIREWALL = 63
VIR_WAR_NO_SECRET = 64
VIR_ERR_INVALID_SECRET = 65
VIR_ERR_NO_SECRET = 66
VIR_ERR_CONFIG_UNSUPPORTED = 67
VIR_ERR_OPERATION_TIMEOUT = 68
VIR_ERR_MIGRATE_PERSIST_FAILED = 69
VIR_ERR_HOOK_SCRIPT_FAILED = 70
VIR_ERR_INVALID_DOMAIN_SNAPSHOT = 71
VIR_ERR_NO_DOMAIN_SNAPSHOT = 72
VIR_ERR_INVALID_STREAM = 73
VIR_ERR_ARGUMENT_UNSUPPORTED = 74
VIR_ERR_STORAGE_PROBE_FAILED = 75
VIR_ERR_STORAGE_POOL_BUILT = 76
VIR_ERR_SNAPSHOT_REVERT_RISKY = 77
VIR_ERR_OPERATION_ABORTED = 78
VIR_ERR_AUTH_CANCELLED = 79
VIR_ERR_NO_DOMAIN_METADATA = 80
VIR_ERR_MIGRATE_UNSAFE = 81
VIR_ERR_OVERFLOW = 82
VIR_ERR_BLOCK_COPY_ACTIVE = 83
VIR_ERR_OPERATION_UNSUPPORTED = 84
VIR_ERR_SSH = 85
VIR_ERR_AGENT_UNRESPONSIVE = 86
VIR_ERR_RESOURCE_BUSY = 87
VIR_ERR_ACCESS_DENIED = 88
VIR_ERR_DBUS_SERVICE = 89
VIR_ERR_STORAGE_VOL_EXIST = 90

# virEventHandleType
VIR_EVENT_HANDLE_READABLE = 1
VIR_EVENT_HANDLE_WRITABLE = 2
VIR_EVENT_HANDLE_ERROR = 4
VIR_EVENT_HANDLE_HANGUP = 8

# virInterfaceXMLFlags
VIR_INTERFACE_XML_INACTIVE = 1

# virKeycodeSet
VIR_KEYCODE_SET_LINUX = 0
VIR_KEYCODE_SET_XT = 1
VIR_KEYCODE_SET_ATSET1 = 2
VIR_KEYCODE_SET_ATSET2 = 3
VIR_KEYCODE_SET_ATSET3 = 4
VIR_KEYCODE_SET_OSX = 5
VIR_KEYCODE_SET_XT_KBD = 6
VIR_KEYCODE_SET_USB = 7
VIR_KEYCODE_SET_WIN32 = 8
VIR_KEYCODE_SET_RFB = 9

# virMemoryParameterType
VIR_DOMAIN_MEMORY_PARAM_INT = 1
VIR_DOMAIN_MEMORY_PARAM_UINT = 2
VIR_DOMAIN_MEMORY_PARAM_LLONG = 3
VIR_DOMAIN_MEMORY_PARAM_ULLONG = 4
VIR_DOMAIN_MEMORY_PARAM_DOUBLE = 5
VIR_DOMAIN_MEMORY_PARAM_BOOLEAN = 6

# virNetworkEventID
VIR_NETWORK_EVENT_ID_LIFECYCLE = 0

# virNetworkEventLifecycleType
VIR_NETWORK_EVENT_DEFINED = 0
VIR_NETWORK_EVENT_UNDEFINED = 1
VIR_NETWORK_EVENT_STARTED = 2
VIR_NETWORK_EVENT_STOPPED = 3

# virNetworkUpdateCommand
VIR_NETWORK_UPDATE_COMMAND_NONE = 0
VIR_NETWORK_UPDATE_COMMAND_MODIFY = 1
VIR_NETWORK_UPDATE_COMMAND_DELETE = 2
VIR_NETWORK_UPDATE_COMMAND_ADD_LAST = 3
VIR_NETWORK_UPDATE_COMMAND_ADD_FIRST = 4

# virNetworkUpdateFlags
VIR_NETWORK_UPDATE_AFFECT_CURRENT = 0
VIR_NETWORK_UPDATE_AFFECT_LIVE = 1
VIR_NETWORK_UPDATE_AFFECT_CONFIG = 2

# virNetworkUpdateSection
VIR_NETWORK_SECTION_NONE = 0
VIR_NETWORK_SECTION_BRIDGE = 1
VIR_NETWORK_SECTION_DOMAIN = 2
VIR_NETWORK_SECTION_IP = 3
VIR_NETWORK_SECTION_IP_DHCP_HOST = 4
VIR_NETWORK_SECTION_IP_DHCP_RANGE = 5
VIR_NETWORK_SECTION_FORWARD = 6
VIR_NETWORK_SECTION_FORWARD_INTERFACE = 7
VIR_NETWORK_SECTION_FORWARD_PF = 8
VIR_NETWORK_SECTION_PORTGROUP = 9
VIR_NETWORK_SECTION_DNS_HOST = 10
VIR_NETWORK_SECTION_DNS_TXT = 11
VIR_NETWORK_SECTION_DNS_SRV = 12

# virNetworkXMLFlags
VIR_NETWORK_XML_INACTIVE = 1

# virNodeGetCPUStatsAllCPUs
VIR_NODE_CPU_STATS_ALL_CPUS = -1

# virNodeGetMemoryStatsAllCells
VIR_NODE_MEMORY_STATS_ALL_CELLS = -1

# virNodeSuspendTarget
VIR_NODE_SUSPEND_TARGET_MEM = 0
VIR_NODE_SUSPEND_TARGET_DISK = 1
VIR_NODE_SUSPEND_TARGET_HYBRID = 2

# virSchedParameterType
VIR_DOMAIN_SCHED_FIELD_INT = 1
VIR_DOMAIN_SCHED_FIELD_UINT = 2
VIR_DOMAIN_SCHED_FIELD_LLONG = 3
VIR_DOMAIN_SCHED_FIELD_ULLONG = 4
VIR_DOMAIN_SCHED_FIELD_DOUBLE = 5
VIR_DOMAIN_SCHED_FIELD_BOOLEAN = 6

# virSecretUsageType
VIR_SECRET_USAGE_TYPE_NONE = 0
VIR_SECRET_USAGE_TYPE_VOLUME = 1
VIR_SECRET_USAGE_TYPE_CEPH = 2
VIR_SECRET_USAGE_TYPE_ISCSI = 3

# virStoragePoolBuildFlags
VIR_STORAGE_POOL_BUILD_NEW = 0
VIR_STORAGE_POOL_BUILD_REPAIR = 1
VIR_STORAGE_POOL_BUILD_RESIZE = 2
VIR_STORAGE_POOL_BUILD_NO_OVERWRITE = 4
VIR_STORAGE_POOL_BUILD_OVERWRITE = 8

# virStoragePoolDeleteFlags
VIR_STORAGE_POOL_DELETE_NORMAL = 0
VIR_STORAGE_POOL_DELETE_ZEROED = 1

# virStoragePoolState
VIR_STORAGE_POOL_INACTIVE = 0
VIR_STORAGE_POOL_BUILDING = 1
VIR_STORAGE_POOL_RUNNING = 2
VIR_STORAGE_POOL_DEGRADED = 3
VIR_STORAGE_POOL_INACCESSIBLE = 4

# virStorageVolCreateFlags
VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA = 1

# virStorageVolDeleteFlags
VIR_STORAGE_VOL_DELETE_NORMAL = 0
VIR_STORAGE_VOL_DELETE_ZEROED = 1

# virStorageVolResizeFlags
VIR_STORAGE_VOL_RESIZE_ALLOCATE = 1
VIR_STORAGE_VOL_RESIZE_DELTA = 2
VIR_STORAGE_VOL_RESIZE_SHRINK = 4

# virStorageVolType
VIR_STORAGE_VOL_FILE = 0
VIR_STORAGE_VOL_BLOCK = 1
VIR_STORAGE_VOL_DIR = 2
VIR_STORAGE_VOL_NETWORK = 3
VIR_STORAGE_VOL_NETDIR = 4

# virStorageVolWipeAlgorithm
VIR_STORAGE_VOL_WIPE_ALG_ZERO = 0
VIR_STORAGE_VOL_WIPE_ALG_NNSA = 1
VIR_STORAGE_VOL_WIPE_ALG_DOD = 2
VIR_STORAGE_VOL_WIPE_ALG_BSI = 3
VIR_STORAGE_VOL_WIPE_ALG_GUTMANN = 4
VIR_STORAGE_VOL_WIPE_ALG_SCHNEIER = 5
VIR_STORAGE_VOL_WIPE_ALG_PFITZNER7 = 6
VIR_STORAGE_VOL_WIPE_ALG_PFITZNER33 = 7
VIR_STORAGE_VOL_WIPE_ALG_RANDOM = 8

# virStorageXMLFlags
VIR_STORAGE_XML_INACTIVE = 1

# virStreamEventType
VIR_STREAM_EVENT_READABLE = 1
VIR_STREAM_EVENT_WRITABLE = 2
VIR_STREAM_EVENT_ERROR = 4
VIR_STREAM_EVENT_HANGUP = 8

# virStreamFlags
VIR_STREAM_NONBLOCK = 1

# virTypedParameterFlags
VIR_TYPED_PARAM_STRING_OKAY = 4

# virTypedParameterType
VIR_TYPED_PARAM_INT = 1
VIR_TYPED_PARAM_UINT = 2
VIR_TYPED_PARAM_LLONG = 3
VIR_TYPED_PARAM_ULLONG = 4
VIR_TYPED_PARAM_DOUBLE = 5
VIR_TYPED_PARAM_BOOLEAN = 6
VIR_TYPED_PARAM_STRING = 7

# virVcpuState
VIR_VCPU_OFFLINE = 0
VIR_VCPU_RUNNING = 1
VIR_VCPU_BLOCKED = 2

