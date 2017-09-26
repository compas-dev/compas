'''
Created on 10.11.2011

@author: vanmelet
'''

import sys

from matlabIO import MatlabIOClass
import numpy as np
import scipy as sp
from numpy import array,mat,zeros,ones,eye,diag,diagflat,asmatrix,asarray,\
                  concatenate,hstack,vstack,absolute,nonzero,where,\
                  cross,dot,\
                  max,maximum,abs,absolute,power,sqrt
from numpy.linalg import solve,norm,pinv,svd
from scipy.optimize import leastsq,\
                           fmin_slsqp,nnls,fmin_cobyla,fmin_tnc,fmin_l_bfgs_b,\
                           brute

#import pyOpt
#from pyOpt import Optimization
#from pyOpt import SLSQP
#from pyOpt import PSQP
#from pyOpt import CONMIN
#from pyOpt import KSOPT
#from pyOpt import COBYLA
#from pyOpt import SOLVOPT
#from pyOpt import NSGA2

#print np.show_config()
#print sp.show_config()
#sp.test()
#sys.exit()

#===============================================================================
#===============================================================================

np.set_printoptions(linewidth = 1000, threshold = 10000)

#===============================================================================
#===============================================================================

class FormFinderClass(object):
    ''''''
    
    
    
    def __init__(self, **kwargs):
        ''''''
        self.solvers = {
            'LSQLIN'  : self.LSQLIN,
            'PSEARCH' : self.PSEARCH,
            'FMINCON' : self.FMINCON,
            'LEASTSQ' : self.LEASTSQ,
            'LBFGSB'  : self.LBFGSB,
            'LMA'     : self.LMA,
            'SLSQP'   : self.SLSQP,
            'COBYLA'  : self.COBYLA,
            'NNLS'    : self.NNLS,
            'TNC'     : self.TNC,
            'BRUTE'   : self.BRUTE,
#
#            'poSNOPT'   : self.poSNOPT,
#            'poNLPQL'   : self.poNLPQL,
#            'poFSQP'    : self.poFSQP,
#            'poSLSQP'   : self.poSLSQP,
#            'poPSQP'    : self.poPSQP,
#            'poCONMIN'  : self.poCONMIN,
#            'poKSOPT'   : self.poKSOPT,
#            'poCOBYLA'  : self.poCOBYLA,
#            'poSOLVOPT' : self.poSOLVOPT,
        }
#        self.objFuncParams = {
#            'po' : [],
#        }
    
    
    
    def findForm(self, net, q, loads):
        '''
        '''
        C = net.C
        ni = net.ni
        xyz = net.xyz

        Ci = C[:,:ni]
        Cf = C[:,ni:]
        
        xf = xyz[ni:,0]
        yf = xyz[ni:,1]
        zf = xyz[ni:,2]

        px = loads[:,0]
        py = loads[:,1]
        pz = loads[:,2]
        
        pxi = px[:ni,0]
        pyi = py[:ni,0]
        pzi = pz[:ni,0]
        
        Q = diag(q.flat)
        D = Ci.T * Q * Ci
        Df = Ci.T * Q * Cf
        
        x = solve(D, pxi - Df * xf)
        y = solve(D, pyi - Df * yf)
        z = solve(D, pzi - Df * zf)
        
        free = concatenate((x,y,z), 1)
        fixed = concatenate((xf,yf,zf), 1)
        xyz = concatenate((free, fixed), 0)
        net.xyz = xyz
        net.q = q
        return xyz
    
    
    
    def findClosestFit(self, method, net, loads, qind0, zT):
        '''Wrapper for the different solver methods.'''
        if method not in self.solvers :
            raise Exception('unsupported solver')

        m = net.m
        ni = net.ni
        xyz = net.xyz
        dof = net.dof
        ind = net.ind
        C = net.C
        C_ = net.C_
        E = net.E
        bc = net.bc

        Ed = E[:,:m-dof]
        Eind = E[:,m-dof:]
        EE = -pinv(Ed)*Eind
        EEE = vstack((EE,eye(dof)))
        
        Ci = C[:,:ni]
        Cf = C[:,ni:]
        
        x = xyz[:,0]
        y = xyz[:,1]
        z = xyz[:,2]
        xf = x[ni:]
        yf = y[ni:]
        zf = z[ni:]
        xi = x[:ni]
        yi = y[:ni]
        pz = loads[:,2]
        pzi = pz[:ni,0]
        
        # find good starting point
        #=======================================================================
        
        x_ = bc[:,0]
        y_ = bc[:,1]
        u_ = C_*x_
        v_ = C_*y_
        l_ = np.sqrt(np.power(u_,2) + np.power(v_,2))
        u = C*x
        v = C*y
        l = np.sqrt(np.power(u,2) + np.power(v,2))
        
        q_ = -l_/l
        qind0_ = q_[net.m-net.dof:]

#        qind0 = qind0_
#        mIO = MatlabIOClass()
#        bound = 0.001*np.min(q_)
#        qind0 = mIO.lsqlin(q_, qind0_, net, bound)
        qind0 = self.solvers['LSQLIN'](qind0_, EE, EEE, q_, dof)
        qind0 = np.squeeze(asarray(qind0))
        
#        print qind0
#        sys.exit()
        
        #=======================================================================
        #=======================================================================
        
        if method == 'FMINCON' or method == 'PSEARCH' :
            opt_res = self.solvers[method](qind0, net, pzi, zT, EEE)
        else :
            # temp solution
            zTi = zT[:ni]
            opt_res = self.solvers[method](qind0, Ci, Cf, EE, EEE, pzi, zf, zTi, dof)
        
        q = opt_res[0]
        Q = diag(q.flat)
        D = Ci.T * Q * Ci
        Df = Ci.T * Q * Cf
        zi = solve(D, pzi - Df * zf)

        x = concatenate((xi,xf),0)
        y = concatenate((yi,yf),0)
        z = concatenate((zi,zf),0)
        xyz = concatenate((x,y,z), 1)
        net.q = q
        net.xyz = xyz
        
        return opt_res
        
    
    
#===============================================================================
#===============================================================================
#===============================================================================


        
    def objfun(self, qind, *args):
        '''Objective function.'''
        Ci = args[0]
        Cf = args[1]
        EE = args[2]
        EEE = args[3]
        pz = args[4]
        zf = args[5]
        zT = args[6]
        
        qind = mat(qind).T
        q = EEE * qind
        Q = diag(q.flat)
        D = Ci.T * Q * Ci
        Df = Ci.T * Q * Cf
        zi = solve(D, pz - Df * zf)
        f = (power(zi - zT, 2)).sum()
        return f
    


    def jacobian(self, qind, *args):
        '''Jacobian.'''
        Ci = args[0]
        Cf = args[1]
        EE = args[2]
        EEE = args[3]
        pz = args[4]
        zf = args[5]
        zT = args[6]
        
        qind = mat(qind).T
        q = EEE * qind
        
        Q = diag(q.flat)
        D = Ci.T * Q * Ci
        Df = Ci.T * Q * Cf
        zi = solve(D, pz - Df * zf)
        
        W = diag((Ci*zi).flat)
        J = solve(-D, Ci.T) * W * EEE
        f = zi - zT
        g = J.T * f
        g = np.squeeze(asarray(g))
        
        return g
    
    
    
    def ieqcons(self, qind, *args):
        '''Inequality constraints.'''
        EE = args[2]
        
        qind = mat(qind).T
        qd = -EE * qind
        qd = np.squeeze(asarray(qd))
        
        return qd
    
    
    
#    def objfun2(self, qind, *args):
#        '''Objective function.'''
#        Ci = args[0]
#        Cf = args[1]
#        EE = args[2]
#        EEE = args[3]
#        pz = args[4]
#        zf = args[5]
#        zT = args[6]
#        
#        qind = mat(qind).T
#        q = EEE * qind
#        Q = diag(q.flat)
#        D = Ci.T * Q * Ci
#        Df = Ci.T * Q * Cf
#        zi = solve(D, pz - Df * zf)
#        g = zi - zT
#        g = np.squeeze(asarray(g))
#        
#        return g
#    
#
#
#    def jacobian2(self, qind, *args):
#        '''Jacobian.'''
#        Ci = args[0]
#        Cf = args[1]
#        EE = args[2]
#        EEE = args[3]
#        pz = args[4]
#        zf = args[5]
#        zT = args[6]
#        
#        qind = mat(qind).T
#        q = EEE * qind
#        
#        Q = diag(q.flat)
#        D = Ci.T * Q * Ci
#        Df = Ci.T * Q * Cf
#        zi = solve(D, pz - Df * zf)
#        
#        W = diag((Ci*zi).flat)
#        J = solve(-D, Ci.T) * W * EEE
#        f = zi - zT
#        g = J.T * f
#        g = np.squeeze(asarray(g))
#        
#        return g

    

#===============================================================================
#===============================================================================
#===============================================================================


    def PSEARCH(self, qind0, net, pz, zT, EEE):
        ''''''
        mIO = MatlabIOClass()
        optres = mIO.psearch(qind0, net, pz, zT)

        qind = optres
        qind = mat(qind).T
        q = EEE * qind
        return [q]

        

    def FMINCON(self, qind0, net, pz, zT, EEE):
        ''''''
        mIO = MatlabIOClass()
        optres = mIO.fmincon(qind0, net, pz, zT)

        qind = optres
        qind = mat(qind).T
        q = EEE * qind
        return [q]

        
#===============================================================================
#===============================================================================
#===============================================================================


        
    def LMA(self, qind0, Ci, Cf, EE, EEE, pz, zf, zT, dof):
        '''Self-implemented Levenbergh-Marquardt algorithm.'''
        qind0 = mat(qind0).T
        q = EEE * qind0
        
        Q = diag(q.flat)
        D = Ci.T * Q * Ci
        Df = Ci.T * Q * Cf
        zi = solve(D, pz - Df * zf)
        
        W = diag((Ci*zi).flat)
        J = solve(-D, Ci.T) * W * EEE
        A = J.T * J
        a = diag(A)
        f = zi - zT
        g = J.T * f
        
        tau = 1e-06
        eps1 = 1e-08
        eps2 = 1e-08
        kmax = 1000
        k = 0
        v = 2
        mu = tau * max(a)
        
        stop = 'max(abs(g)): %s > %s' % (max(abs(g)), eps1)
        while max(abs(g)) > eps1 :
            dqind = solve(-(A + mu * eye(dof)), g)
            dq = EEE * dqind
            # differences between iterations become too small
            # this means that we are at a local minimum, i think
            if norm(dq) <= eps2 * norm(q) :
                stop = 'differences: %s <= %s' % (norm(dq),eps2*norm(q))
                break
            qn = q + dq
            # linear force density
            Q = diag(qn.flat)
            D = Ci.T * Q * Ci
            Df = Ci.T * Q * Cf
            zi = solve(D, pz - Df * zf)
            # current difference
            fn = zi - zT
            # gain ratio
            # assess whether to switch between ...
            gain = (0.5 * (sum(power(f,2)) - sum(power(fn,2)))) / (0.5 * dqind.T * (mu * dqind - g))
            if gain > 0 :
                # ...
                q = qn
                Q = diag(q.flat)
                D = Ci.T * Q * Ci
                Df = Ci.T * Q * Cf
                zi = solve(D, pz - Df * zf)
                
                W = diag((Ci*zi).flat)
                J = solve(-D, Ci.T) * W * EEE
                A = J.T * J
                a = diag(A)
                f = zi - zT
                g = J.T * f
                
                mu = mu * max([1/3,1-(2*gain-1)**3])
                v = 2
            else :
                # ...
                mu = mu * v
                v = 2 * v
            k = k + 1
            if k >= kmax :
                stop = 'kmax'
                break
        return [q, stop, k, g]
        
    
    
#===============================================================================
#===============================================================================
#===============================================================================

    
    
    def LEASTSQ(self, qind0, Ci,Cf,EE,EEE,pz,zf,zT,dof):
        '''Sequential Least SQuares Programming.'''
        optres = leastsq(self.objfun2, 
                         qind0, 
                         args=(Ci,Cf,EE,EEE,pz,zf,zT), 
                         Dfun=self.jacobian, 
                         full_output=1, 
                         col_deriv=0, 
                         ftol=1.49012e-08, 
                         xtol=1.49012e-08, 
                         gtol=0.0, 
                         maxfev=0, 
                         epsfcn=0.0, 
                         factor=100, 
                         diag=None)
        qind = optres[0]
        qind = mat(qind).T
        q = EEE * qind
        return [q]

    
    
#===============================================================================
#===============================================================================
#===============================================================================


    def LSQLIN(self, qind0, EE, EEE, q0, dof):
        ''''''
#        qind_bounds = [(0,None) for i in range(dof)]
#        qind_bounds = [(0,100) for i in range(dof)]
        qind_bounds = []
        optres = fmin_slsqp(self.objfun3, 
                            qind0, 
                            eqcons=[], 
                            f_eqcons=None, 
                            ieqcons=[], 
                            f_ieqcons=self.ieqcons3, 
                            bounds=qind_bounds, 
                            fprime=None, 
                            fprime_eqcons=None, 
                            fprime_ieqcons=None, 
                            args=(EE,EEE,q0), 
                            iter=10000, 
                            acc=1e-06, 
                            iprint=1, 
                            disp=2, 
                            full_output=1, 
                            epsilon=1.4901161193847656e-08)
        qind = optres[0]
        qind = mat(qind).T
        return qind
    
    
    def objfun3(self, qind, *args):
        ''''''
        EEE = args[1]
        q0 = args[2]
        
        qind = mat(qind).T
        q = EEE * qind
        f = 0.5 * (power(q - q0, 2)).sum()
        return f

    
    def ieqcons3(self, qind, *args):
        '''Inequality constraints.'''
        EE = args[0]
        
        qind = mat(qind).T
        qd = -EE * qind
        qd = np.squeeze(asarray(qd))
        
        return qd
    
    
#===============================================================================
#===============================================================================
#===============================================================================

    
    def LBFGSB(self, qind0, Ci,Cf,EE,EEE,pz,zf,zT,dof):
        '''L-BFGS-B'''
#        qind_bounds = [(0,None) for i in range(dof)]
        qind_bounds = None
        optres = fmin_l_bfgs_b(self.objfun, 
                               qind0, 
                               fprime=self.jacobian, 
                               args=(Ci,Cf,EE,EEE,pz,zf,zT), 
                               approx_grad=0, 
                               bounds=qind_bounds, 
                               m=10, 
                               factr=10.0, 
                               pgtol=1e-05, 
                               epsilon=1e-08, 
                               iprint=0, 
                               maxfun=15000, 
                               disp=3)
        qind = optres[0]
        qind = mat(qind).T
        q = EEE * qind
        return [q]

    
    
    def SLSQP(self, qind0, Ci,Cf,EE,EEE,pz,zf,zT,dof):
        '''Sequential Least SQuares Programming.'''
#        qind_bounds = [(0,100) for i in range(dof)]
        qind_bounds = []
        optres = fmin_slsqp(self.objfun, 
                            qind0, 
                            eqcons=[], 
                            f_eqcons=None, 
                            ieqcons=[], 
                            f_ieqcons=self.ieqcons, 
                            bounds=qind_bounds, 
                            fprime=self.jacobian, 
                            fprime_eqcons=None, 
                            fprime_ieqcons=None, 
                            args=(Ci,Cf,EE,EEE,pz,zf,zT), 
                            iter=10000, 
                            acc=1e-06, 
                            iprint=1, 
                            disp=2, 
                            full_output=1, 
                            epsilon=1.4901161193847656e-08)
        qind = optres[0]
        qind = mat(qind).T
        q = EEE * qind
        return [q]
    
    
    def NNLS(self, qind0, Ci,Cf,EE,EEE,pz,zf,zT,dof):
        '''Find the closest fit using a non-negative least squares solver.
        Solve argmin_x || Ax - b ||_2 for x>=0. 
        This is a wrapper for a FORTAN non-negative least squares solver.'''
        return
    
    
    
    def COBYLA(self, qind0, Ci,Cf,EE,EEE,pz,zf,zT,dof):
        '''Constrained optimization by linear approximation.'''
        optres = fmin_cobyla(self.objfun, 
                             qind0, 
                             cons=self.ieqcons, 
                             args=(Ci,Cf,EE,EEE,pz,zf,zT), 
                             consargs=None, 
                             rhobeg=1.0, 
                             rhoend=0.0001, 
                             iprint=1, 
                             maxfun=5000, 
                             disp=2)
        qind = optres
        qind = mat(qind).T
        q = EEE * qind
        return [q]
    
    
    
    def TNC(self, qind0, Ci,Cf,EE,EEE,pz,zf,zT,dof):
        '''Truncated Newton algorithm.'''
        qind_bounds = [(0,None) for i in range(dof)]
        optres = fmin_tnc(self.objfun, 
                          qind0, 
                          fprime=self.jacobian, 
                          args=(Ci,Cf,EE,EEE,pz,zf,zT), 
                          approx_grad=0, 
                          bounds=qind_bounds, 
                          epsilon=1e-08, 
                          scale=None, 
                          offset=None, 
                          messages=15, 
                          maxCGit=-1, 
                          maxfun=None, 
                          eta=-1, 
                          stepmx=0, 
                          accuracy=0, 
                          fmin=0, 
                          ftol=-1, 
                          xtol=-1, 
                          pgtol=-1, 
                          rescale=-1, 
                          disp=5)
        qind = optres[0]
        qind = mat(qind).T
        q = EEE * qind
        return [q]



    def BRUTE(self, qind0, Ci,Cf,EE,EEE,pz,zf,zT,dof):
        '''Brute force...
        Maximum 40 variables.'''
        ranges = [(0,20) for i in range(dof)]
        optres = brute(self.objfun, 
                       ranges, 
                       args=(Ci,Cf,EE,EEE,pz,zf,zT), 
                       Ns=20, 
                       full_output=0, 
                       finish=None)
        qind = optres[0]
        qind = mat(qind).T
        q = EEE * qind
        return [q]



##===============================================================================
##===============================================================================
##===============================================================================
#
#
#
#    def poSNOPT(self, qind0, Ci, Cf, EE, pz, zf, zT, dof):
#        ''''''
#        opt_prob = Optimization('', self.poObjFunc)
#        opt_prob.addObj('f')
#        opt_prob.addVarGroup('qind', len(qind0), 'c', value=qind0, lower=0.0, upper=100)
#        opt_prob.addConGroup('g',1,'i')
#        
#        opt = pyOpt.SNOPT()
#        opt_sol = opt(opt_prob, 
#                      sens_type='FD', 
#                      store_sol=True, 
#                      disp_opts=False, 
#                      store_hst=False, hot_start=False, 
#                      sens_mode='', sens_step={})
#        
#        qind = mat(opt_sol[1]).T
#        q = EE * qind
#        
#        return [q, opt_prob]
#
#
#        
#    def poNLPQL(self, qind0, Ci, Cf, EE, pz, zf, zT, dof):
#        ''''''
#        opt_prob = Optimization('', self.poObjFunc)
#        opt_prob.addObj('f')
#        opt_prob.addVarGroup('qind', len(qind0), 'c', value=qind0, lower=0.0, upper=100)
#        opt_prob.addConGroup('g',1,'i')
#        
#        opt = pyOpt.NLPQL()
#        opt_sol = opt(opt_prob, 
#                      sens_type='FD', 
#                      store_sol=True, 
#                      disp_opts=False, 
#                      store_hst=False, hot_start=False, 
#                      sens_mode='', sens_step={})
#        
#        qind = mat(opt_sol[1]).T
#        q = EE * qind
#        
#        return [q, opt_prob]
#
#
#        
#    def poFSQP(self, qind0, Ci, Cf, EE, pz, zf, zT, dof):
#        ''''''
#        opt_prob = Optimization('', self.poObjFunc)
#        opt_prob.addObj('f')
#        opt_prob.addVarGroup('qind', len(qind0), 'c', value=qind0, lower=0.0, upper=100)
#        opt_prob.addConGroup('g',1,'i')
#        
#        opt = pyOpt.FSQP()
#        opt_sol = opt(opt_prob, 
#                      sens_type='FD', 
#                      store_sol=True, store_hst=False, 
#                      hot_start=False, 
#                      disp_opts=False, 
#                      sens_mode='', sens_step={})
#        
#        qind = mat(opt_sol[1]).T
#        q = EE * qind
#        
#        return [q, opt_prob]
#
#
#
#    def poSLSQP(self, qind0, Ci, Cf, EE, pz, zf, zT, dof):
#        ''''''
#        opt_prob = Optimization('', self.poObjFunc)
#        opt_prob.addObj('f')
#        opt_prob.addVarGroup('qind', len(qind0), 'c', value=qind0, lower=0.0, upper=100)
#        opt_prob.addConGroup('g',1,'i')
#        
#        opt = SLSQP()
#        opt_sol = opt(opt_prob,
#                      sens_type='FD', 
#                      store_sol=True, 
#                      disp_opts=False, 
#                      store_hst=False, hot_start=False, 
#                      sens_mode='', sens_step={})
#        
#        qind = mat(opt_sol[1]).T
#        q = EE * qind
#        
#        return [q, opt_prob]
#
#
#        
#    def poPSQP(self, qind0, Ci, Cf, EE, pz, zf, zT, dof):
#        ''''''
#        opt_prob = Optimization('', self.poObjFunc)
#        opt_prob.addObj('f')
#        opt_prob.addVarGroup('qind', len(qind0), 'c', value=qind0, lower=0.0, upper=100)
#        opt_prob.addConGroup('g',1,'i')
#        
#        opt = PSQP()
#        opt_sol = opt(opt_prob,
#                      sens_type='FD', 
#                      store_sol=True, 
#                      disp_opts=False, 
#                      store_hst=False, hot_start=False, 
#                      sens_mode='', sens_step={})
#        
#        qind = mat(opt_sol[1]).T
#        q = EE * qind
#        
#        return [q, opt_prob]
#
#
#        
#    def poCONMIN(self, qind0, Ci, Cf, EE, pz, zf, zT, dof):
#        ''''''
#        opt_prob = Optimization('', self.poObjFunc)
#        opt_prob.addObj('f')
#        opt_prob.addVarGroup('qind', len(qind0), 'c', value=qind0, lower=0.0, upper=100)
#        opt_prob.addConGroup('g',1,'i')
#        
#        opt = CONMIN()
#        opt_sol = opt(opt_prob, 
#                      sens_type='CS', 
#                      store_sol=True, store_hst=False, 
#                      hot_start=False, 
#                      disp_opts=False, 
#                      sens_mode='', sens_step={})
#        
#        qind = mat(opt_sol[1]).T
#        q = EE * qind
#        
#        return [q, opt_prob]
#
#
#
#    def poKSOPT(self, qind0, Ci, Cf, EE, pz, zf, zT, dof):
#        ''''''
#        opt_prob = Optimization('', self.poObjFunc)
#        opt_prob.addObj('f')
#        opt_prob.addVarGroup('qind', len(qind0), 'c', value=qind0, lower=0.0, upper=100)
#        opt_prob.addConGroup('g',1,'i')
#        
#        opt = KSOPT()
#        opt_sol = opt(opt_prob, 
#                      sens_type='FD', 
#                      store_sol=True, store_hst=False, 
#                      hot_start=False, 
#                      disp_opts=False, 
#                      sens_mode='', sens_step={})
#        
#        qind = mat(opt_sol[1]).T
#        q = EE * qind
#        
#        return [q, opt_prob]
#
#
#
#    def poCOBYLA(self, qind0, Ci, Cf, EE, pz, zf, zT, dof):
#        ''''''
#        opt_prob = Optimization('', self.poObjFunc)
#        opt_prob.addObj('f')
#        opt_prob.addVarGroup('qind', len(qind0), 'c', value=qind0, lower=0.0, upper=100)
#        opt_prob.addConGroup('g',1,'i')
#        
#        opt = COBYLA()
#        opt_sol = opt(opt_prob, 
#                      store_sol=True, 
#                      disp_opts=False, 
#                      store_hst=False, hot_start=False)
#        
#        qind = mat(opt_sol[1]).T
#        q = EE * qind
#        
#        return [q, opt_prob]
#
#
#        
#    def poSOLVOPT(self, qind0, Ci, Cf, EE, pz, zf, zT, dof):
#        ''''''
#        opt_prob = Optimization('', self.poObjFunc)
#        opt_prob.addObj('f')
#        opt_prob.addVarGroup('qind', len(qind0), 'c', value=qind0, lower=0.0, upper=100)
#        opt_prob.addConGroup('g',1,'i')
#        
#        opt = SOLVOPT()
#        opt_sol = opt(opt_prob, 
#                      sens_type='FD', 
#                      store_sol=True, store_hst=False, 
#                      hot_start=False, 
#                      disp_opts=False, 
#                      sens_mode='', sens_step={})
#        
#        qind = mat(opt_sol[1]).T
#        q = EE * qind
#        
#        return [q, opt_prob]
#
#
#        
##===============================================================================
##===============================================================================
##===============================================================================
#
#
#
#    def poObjFunc(self, qind):
#        ''''''
#        args = self.objFuncParams['po']
#        
#        Ci = args[0]
#        Cf = args[1]
#        EE = args[2]
#        pz = args[3]
#        zf = args[4]
#        zT = args[5]
#        
#        qind = mat(qind).T
#        
#        q = EE * qind
#        Q = diag(q.flat)
#        D = Ci.T * Q * Ci
#        Df = Ci.T * Q * Cf
#        zi = solve(D, pz - Df * zf)
#        
#        q = EE * qind
#
#        f = (power(zi - zT, 2)).sum()
#        g = [0.0]
#        g[0] = -min(q)
#        
#        fail = 0
#        
#        return f, g, fail
#
#    
#    