from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy.sparse import diags
from scipy.linalg import solve
import numpy as np
import logging
import os
import time


"""
Orginal work Written by Krister Svanberg in Matlab. This is the python version of the code written
by Arjen Deetman.

"""

__all__ = ['mma_numpy']


def mma_numpy(f_g_eval, f_df_g_dg_eval, x0, bounds, args=(), kkttol=1e-6, maxoutit=100, plot='2'):
    """Method of Moving Asymptotes (MMA) implementation from K. Svanberg.

    Parameters
    ----------
    f_g_eval : callable
        The function used by the minimizer to evaluate the objective function (f)
        and the constraints (g). It takes as input the point to evaluate (x), and the
        arguments (args). It returns two arrays, one for the evaluation of (f-1x1 array)
        and one for the evaluation of (g-mx1 array).
    f_df_g_dg_eval : callable
        The function used by the minimizer to evaluate the objective function (f)
        and the constraints (g) and its derivatives. It takes as input the point to evaluate
        (x), and the arguments (args). It returns four arrays, first the evaluation of
        (f - 1x1 array) and (dfdx - nx1 array), and also the evaluation of (g - mx1 array)
        and its derivative (dgdx - mxn array).
    x0 :  array
        Starting point for the MMA optimisation.
    bounds: list
        Bounds for each variable of the optimisation.
    args: tuple
        Argument to be passed with the callables.
    kkttol : float [10e-6]
        The tolerance for the KKT check, i.e. the tolerance for the stopping point observing
        the null derivatives.
    maxoutit : int [100]
        Maximum number of iterations to perform in the optimisation.
    plot : int [2]
        Control plots on screen. '0' nothing is plot, '1' detailled plot and '2' summary plot.

    Returns
    -------
    fopt : float
        The value of the minimisation.
    xval : array
        Value of the variables on the optimum.

    Notes
    -----
    For more info, see [1]. This is the python version of the code written by Arjen Deetman [2].

    References
    ----------
    .. [1] Svanberg, K., *The method of moving asymptotes–a new method for structural optimization*,
           International Journal for Numerical Methods in Engineering, 24, 359-373, 1987.
    .. [2] Deetman A. *GCMMA-MMA-Python*. https://github.com/arjendeetman/GCMMA-MMA-Python

    """

    lower = np.array([lw[0] for lw in bounds]).reshape(-1, 1)
    upper = np.array([up[1] for up in bounds]).reshape(-1, 1)

    # Start Time
    start_time = time.time()

    # Logger
    path = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(path, "GCMMA_TEST.log")
    logger = setup_logger(file)
    logger.info("Started\n")
    # Set numpy print options
    np.set_printoptions(precision=4, formatter={'float': '{: 0.4f}'.format})
    # Beam initial settings
    f0val, g0 = f_g_eval(x0, *args)
    m = len(g0)
    n = len(x0)
    epsimin = 0.0000001
    eeem = np.ones((m, 1))
    zerom = np.zeros((m, 1))
    xval = x0
    xold1 = xval.copy()
    xold2 = xval.copy()
    xmin = lower  # eeen.copy()
    xmax = upper  # 10*eeen
    low = xmin.copy()
    upp = xmax.copy()
    c = 1000*eeem
    d = eeem.copy()
    a0 = 1
    a = zerom.copy()
    raa0 = 0.01
    raa = 0.01*eeem
    raa0eps = 0.000001
    raaeps = 0.000001*eeem
    outeriter = 0
    maxoutit = 50
    kkttol = kkttol
    maxoutit = maxoutit

    # Calculate function values and gradients of the objective and constraints functions
    if outeriter == 0:
        f0val, df0dx, fval, dfdx = f_df_g_dg_eval(xval, *args)
        innerit = 0
        outvector1 = np.array([outeriter, innerit, f0val, fval])
        outvector2 = xval.flatten()
        # Log
        if plot == '0':
            pass
        elif plot == '2':
            logger.info("Starting Objective Value = {}\n".format(f0val))
        else:
            logger.info("outvector1 = {}".format(outvector1))
            logger.info("outvector2 = {}\n".format(outvector2))
    # The iterations starts
    kktnorm = kkttol + 10
    outit = 0
    while (kktnorm > kkttol) and (outit < maxoutit):
        outit += 1
        outeriter += 1
        if plot != '0':
            logger.info("iteration = {}".format(outit))
        # The parameters low, upp, raa0 and raa are calculated:
        low, upp, raa0, raa = \
            asymp(outeriter, n, xval, xold1, xold2, xmin, xmax, low, upp, raa0, raa, raa0eps, raaeps, df0dx, dfdx)
        # The MMA subproblem is solved at the point xval:
        xmma, ymma, zmma, lam, xsi, eta, mu, zet, s, f0app, fapp = \
            gcmmasub(m, n, iter, epsimin, xval, xmin, xmax, low, upp,
                     raa0, raa, f0val, df0dx, fval, dfdx, a0, a, c, d)
        # The user should now calculate function values (no gradients) of the objective- and constraint
        # functions at the point xmma ( = the optimal solution of the subproblem).
        f0valnew, fvalnew = f_g_eval(xmma, *args)
        # It is checked if the approximations are conservative:
        conserv = concheck(m, epsimin, f0app, f0valnew, fapp, fvalnew)
        # While the approximations are non-conservative (conserv=0), repeated inner iterations are made:
        innerit = 0
        if conserv == 0:
            while conserv == 0 and innerit <= 15:
                innerit += 1
                # New values on the parameters raa0 and raa are calculated:
                raa0, raa = raaupdate(xmma, xval, xmin, xmax, low, upp, f0valnew, fvalnew, f0app, fapp, raa0,
                                      raa, raa0eps, raaeps, epsimin)
                # The GCMMA subproblem is solved with these new raa0 and raa:
                xmma, ymma, zmma, lam, xsi, eta, mu, zet, s, f0app, fapp = gcmmasub(m, n, iter, epsimin, xval, xmin,
                                                                                    xmax, low, upp, raa0, raa, f0val, df0dx, fval, dfdx, a0, a, c, d)
                # The user should now calculate function values (no gradients) of the objective- and
                # constraint functions at the point xmma ( = the optimal solution of the subproblem).
                f0valnew, fvalnew = f_g_eval(xmma, *args)
                # It is checked if the approximations have become conservative:
                conserv = concheck(m, epsimin, f0app, f0valnew, fapp, fvalnew)
        # Some vectors are updated:
        xold2 = xold1.copy()
        xold1 = xval.copy()
        xval = xmma.copy()
        # Re-calculate function values and gradients of the objective and constraints functions
        f0val, df0dx, fval, dfdx = f_df_g_dg_eval(xval, *args)
        # The residual vector of the KKT conditions is calculated
        residu, kktnorm, residumax = \
            kktcheck(m, n, xmma, ymma, zmma, lam, xsi, eta, mu, zet,
                     s, xmin, xmax, df0dx, fval, dfdx, a0, a, c, d)
        outvector1 = np.array([outeriter, innerit, f0val, fval])
        outvector2 = xval.flatten()
        # Log
        if plot == '0':
            pass
        elif plot == '2':
            logger.info("kktnorm    = {}".format(kktnorm))
            logger.info("Objective Iteration: {}\n".format(f0val))
        else:
            logger.info("outvector1 = {}".format(outvector1))
            logger.info("outvector2 = {}".format(outvector2))
            logger.info("kktnorm    = {}".format(kktnorm))
            logger.info("Objective Iteration: {}\n".format(f0val))
    # Final log
    elapsed_time = time.time() - start_time
    logger.info("Finished")
    if kktnorm < kkttol:
        logger.info('Optimisation Terminated Sucessfully.')
        exitflag = 0
    else:
        logger.info('Optimisation did not respect KKT conditions.')
        exitflag = 1
        if outit == maxoutit:
            logger.info('Maximum iterations reached.')
            exitflag = 2
    logger.info("Objective Value: {}".format(f0val))
    logger.info("Total Iterations: {}".format(outeriter))
    print('Elapsed Time: {0:.1f} sec'.format(elapsed_time))

    return f0val, xval, exitflag


def mmasub(m, n, iter, xval, xmin, xmax, xold1, xold2, f0val, df0dx, fval, dfdx, low, upp, a0, a, c, d, move):
    """
    This function mmasub performs one MMA-iteration, aimed at solving the nonlinear programming problem:

    Minimize    f_0(x) + a_0*z + sum( c_i*y_i + 0.5*d_i*(y_i)^2 )
    subject to  f_i(x) - a_i*z - y_i <= 0,  i = 1,...,m
                xmin_j <= x_j <= xmax_j,    j = 1,...,n
                z >= 0,   y_i >= 0,         i = 1,...,m
    INPUT:

        m     = The number of general constraints.
        n     = The number of variables x_j.
        iter  = Current iteration number ( =1 the first time mmasub is called).
        xval  = Column vector with the current values of the variables x_j.
        xmin  = Column vector with the lower bounds for the variables x_j.
        xmax  = Column vector with the upper bounds for the variables x_j.
        xold1 = xval, one iteration ago (provided that iter>1).
        xold2 = xval, two iterations ago (provided that iter>2).
        f0val = The value of the objective function f_0 at xval.
        df0dx = Column vector with the derivatives of the objective function
                f_0 with respect to the variables x_j, calculated at xval.
        fval  = Column vector with the values of the constraint functions f_i, calculated at xval.
        dfdx  = (m x n)-matrix with the derivatives of the constraint functions
                f_i with respect to the variables x_j, calculated at xval.
                dfdx(i,j) = the derivative of f_i with respect to x_j.
        low   = Column vector with the lower asymptotes from the previous
                iteration (provided that iter>1).
        upp   = Column vector with the upper asymptotes from the previous
                iteration (provided that iter>1).
        a0    = The constants a_0 in the term a_0*z.
        a     = Column vector with the constants a_i in the terms a_i*z.
        c     = Column vector with the constants c_i in the terms c_i*y_i.
        d     = Column vector with the constants d_i in the terms 0.5*d_i*(y_i)^2.

    OUTPUT:

        xmma  = Column vector with the optimal values of the variables x_j
                in the current MMA subproblem.
        ymma  = Column vector with the optimal values of the variables y_i
                in the current MMA subproblem.
        zmma  = Scalar with the optimal value of the variable z
                in the current MMA subproblem.
        lam   = Lagrange multipliers for the m general MMA constraints.
        xsi   = Lagrange multipliers for the n constraints alfa_j - x_j <= 0.
        eta   = Lagrange multipliers for the n constraints x_j - beta_j <= 0.
        mu    = Lagrange multipliers for the m constraints -y_i <= 0.
        zet   = Lagrange multiplier for the single constraint -z <= 0.
        s     = Slack variables for the m general MMA constraints.
        low   = Column vector with the lower asymptotes, calculated and used
                in the current MMA subproblem.
        upp   = Column vector with the upper asymptotes, calculated and used
                in the current MMA subproblem.
    """

    epsimin = 0.0000001
    raa0 = 0.00001
    albefa = 0.1
    asyinit = 0.5
    asyincr = 1.2
    asydecr = 0.7
    eeen = np.ones((n, 1))
    eeem = np.ones((m, 1))
    zeron = np.zeros((n, 1))
    # Calculation of the asymptotes low and upp
    if iter <= 2:
        low = xval-asyinit*(xmax-xmin)
        upp = xval+asyinit*(xmax-xmin)
    else:
        zzz = (xval-xold1)*(xold1-xold2)
        factor = eeen.copy()
        factor[np.where(zzz > 0)] = asyincr
        factor[np.where(zzz < 0)] = asydecr
        low = xval-factor*(xold1-low)
        upp = xval+factor*(upp-xold1)
        lowmin = xval-10*(xmax-xmin)
        lowmax = xval-0.01*(xmax-xmin)
        uppmin = xval+0.01*(xmax-xmin)
        uppmax = xval+10*(xmax-xmin)
        low = np.maximum(low, lowmin)
        low = np.minimum(low, lowmax)
        upp = np.minimum(upp, uppmax)
        upp = np.maximum(upp, uppmin)
    # Calculation of the bounds alfa and beta
    zzz1 = low+albefa*(xval-low)
    zzz2 = xval-move*(xmax-xmin)
    zzz = np.maximum(zzz1, zzz2)
    alfa = np.maximum(zzz, xmin)
    zzz1 = upp-albefa*(upp-xval)
    zzz2 = xval+move*(xmax-xmin)
    zzz = np.minimum(zzz1, zzz2)
    beta = np.minimum(zzz, xmax)
    # Calculations of p0, q0, P, Q and b
    xmami = xmax-xmin
    xmamieps = 0.00001*eeen
    xmami = np.maximum(xmami, xmamieps)
    xmamiinv = eeen/xmami
    ux1 = upp-xval
    ux2 = ux1*ux1
    xl1 = xval-low
    xl2 = xl1*xl1
    uxinv = eeen/ux1
    xlinv = eeen/xl1
    p0 = zeron.copy()
    q0 = zeron.copy()
    p0 = np.maximum(df0dx, 0)
    q0 = np.maximum(-df0dx, 0)
    pq0 = 0.001*(p0+q0)+raa0*xmamiinv
    p0 = p0+pq0
    q0 = q0+pq0
    p0 = p0*ux2
    q0 = q0*xl2
    P = np.zeros((m, n))  # @@ make sparse with scipy?
    Q = np.zeros((m, n))  # @@ make sparse with scipy?
    P = np.maximum(dfdx, 0)
    Q = np.maximum(-dfdx, 0)
    PQ = 0.001*(P+Q)+raa0*np.dot(eeem, xmamiinv.T)
    P = P+PQ
    Q = Q+PQ
    P = (diags(ux2.flatten(), 0).dot(P.T)).T
    Q = (diags(xl2.flatten(), 0).dot(Q.T)).T
    b = (np.dot(P, uxinv)+np.dot(Q, xlinv)-fval)
    # Solving the subproblem by a primal-dual Newton method
    xmma, ymma, zmma, lam, xsi, eta, mu, zet, s = subsolv(m, n, epsimin, low, upp, alfa, beta, p0, q0, P, Q, a0, a, b, c, d)
    # Return values
    return xmma, ymma, zmma, lam, xsi, eta, mu, zet, s, low, upp

# Function for the GCMMA sub problem


def gcmmasub(m, n, iter, epsimin, xval, xmin, xmax, low, upp, raa0, raa, f0val, df0dx, fval, dfdx, a0, a, c, d):
    eeen = np.ones((n, 1))
    zeron = np.zeros((n, 1))
    # Calculations of the bounds alfa and beta
    albefa = 0.1
    zzz = low+albefa*(xval-low)
    alfa = np.maximum(zzz, xmin)
    zzz = upp-albefa*(upp-xval)
    beta = np.minimum(zzz, xmax)
    # Calculations of p0, q0, r0, P, Q, r and b.
    xmami = xmax-xmin
    xmamieps = 0.00001*eeen
    xmami = np.maximum(xmami, xmamieps)
    xmamiinv = eeen/xmami
    ux1 = upp-xval
    ux2 = ux1*ux1
    xl1 = xval-low
    xl2 = xl1*xl1
    uxinv = eeen/ux1
    xlinv = eeen/xl1
    #
    p0 = zeron.copy()
    q0 = zeron.copy()
    p0 = np.maximum(df0dx, 0)
    q0 = np.maximum(-df0dx, 0)
    pq0 = p0+q0
    p0 = p0+0.001*pq0
    q0 = q0+0.001*pq0
    p0 = p0+raa0*xmamiinv
    q0 = q0+raa0*xmamiinv
    p0 = p0*ux2
    q0 = q0*xl2
    r0 = f0val-np.dot(p0.T, uxinv)-np.dot(q0.T, xlinv)
    #
    P = np.zeros((m, n))  # @@ make sparse with scipy?
    Q = np.zeros((m, n))  # @@ make sparse with scipy
    P = (diags(ux2.flatten(), 0).dot(P.T)).T
    Q = (diags(xl2.flatten(), 0).dot(Q.T)).T
    b = (np.dot(P, uxinv)+np.dot(Q, xlinv)-fval)
    P = np.maximum(dfdx, 0)
    Q = np.maximum(-dfdx, 0)
    PQ = P+Q
    P = P+0.001*PQ
    Q = Q+0.001*PQ
    P = P+np.dot(raa, xmamiinv.T)
    Q = Q+np.dot(raa, xmamiinv.T)
    P = (diags(ux2.flatten(), 0).dot(P.T)).T
    Q = (diags(xl2.flatten(), 0).dot(Q.T)).T
    r = fval-np.dot(P, uxinv)-np.dot(Q, xlinv)
    b = -r
    # Solving the subproblem by a primal-dual Newton method
    xmma, ymma, zmma, lam, xsi, eta, mu, zet, s = subsolv(m, n, epsimin, low, upp, alfa, beta, p0, q0, P, Q, a0, a, b, c, d)
    # Calculations of f0app and fapp.
    ux1 = upp-xmma
    xl1 = xmma-low
    uxinv = eeen/ux1
    xlinv = eeen/xl1
    f0app = r0+np.dot(p0.T, uxinv)+np.dot(q0.T, xlinv)
    fapp = r+np.dot(P, uxinv)+np.dot(Q, xlinv)
    # Return values
    return xmma, ymma, zmma, lam, xsi, eta, mu, zet, s, f0app, fapp

# Function for solving the subproblem (can be used for MMA and GCMMA)


def subsolv(m, n, epsimin, low, upp, alfa, beta, p0, q0, P, Q, a0, a, b, c, d):
    """
    This function subsolv solves the MMA subproblem:

    minimize SUM[p0j/(uppj-xj) + q0j/(xj-lowj)] + a0*z + SUM[ci*yi + 0.5*di*(yi)^2],

    subject to SUM[pij/(uppj-xj) + qij/(xj-lowj)] - ai*z - yi <= bi,
        alfaj <=  xj <=  betaj,  yi >= 0,  z >= 0.

    Input:  m, n, low, upp, alfa, beta, p0, q0, P, Q, a0, a, b, c, d.
    Output: xmma,ymma,zmma, slack variables and Lagrange multiplers.
    """

    een = np.ones((n, 1))
    eem = np.ones((m, 1))
    epsi = 1
    epsvecn = epsi*een
    epsvecm = epsi*eem
    x = 0.5*(alfa+beta)
    y = eem.copy()
    z = np.array([[1.0]])
    lam = eem.copy()
    xsi = een/(x-alfa)
    xsi = np.maximum(xsi, een)
    eta = een/(beta-x)
    eta = np.maximum(eta, een)
    mu = np.maximum(eem, 0.5*c)
    zet = np.array([[1.0]])
    s = eem.copy()
    itera = 0
    # Start while epsi>epsimin
    while epsi > epsimin:
        epsvecn = epsi*een
        epsvecm = epsi*eem
        ux1 = upp-x
        xl1 = x-low
        ux2 = ux1*ux1
        xl2 = xl1*xl1
        uxinv1 = een/ux1
        xlinv1 = een/xl1
        plam = p0+np.dot(P.T, lam)
        qlam = q0+np.dot(Q.T, lam)
        gvec = np.dot(P, uxinv1)+np.dot(Q, xlinv1)
        dpsidx = plam/ux2-qlam/xl2
        rex = dpsidx-xsi+eta
        rey = c+d*y-mu-lam
        rez = a0-zet-np.dot(a.T, lam)
        relam = gvec-a*z-y+s-b
        rexsi = xsi*(x-alfa)-epsvecn
        reeta = eta*(beta-x)-epsvecn
        remu = mu*y-epsvecm
        rezet = zet*z-epsi
        res = lam*s-epsvecm
        residu1 = np.concatenate((rex, rey, rez), axis=0)
        residu2 = np.concatenate((relam, rexsi, reeta, remu, rezet, res), axis=0)
        residu = np.concatenate((residu1, residu2), axis=0)
        residunorm = np.sqrt((np.dot(residu.T, residu)).item())
        residumax = np.max(np.abs(residu))
        ittt = 0
        # Start while (residumax>0.9*epsi) and (ittt<200)
        while (residumax > 0.9*epsi) and (ittt < 200):
            ittt = ittt+1
            itera = itera+1
            ux1 = upp-x
            xl1 = x-low
            ux2 = ux1*ux1
            xl2 = xl1*xl1
            ux3 = ux1*ux2
            xl3 = xl1*xl2
            uxinv1 = een/ux1
            xlinv1 = een/xl1
            uxinv2 = een/ux2
            xlinv2 = een/xl2
            plam = p0+np.dot(P.T, lam)
            qlam = q0+np.dot(Q.T, lam)
            gvec = np.dot(P, uxinv1)+np.dot(Q, xlinv1)
            GG = (diags(uxinv2.flatten(), 0).dot(P.T)).T-(diags(xlinv2.flatten(), 0).dot(Q.T)).T
            dpsidx = plam/ux2-qlam/xl2
            delx = dpsidx-epsvecn/(x-alfa)+epsvecn/(beta-x)
            dely = c+d*y-lam-epsvecm/y
            delz = a0-np.dot(a.T, lam)-epsi/z
            dellam = gvec-a*z-y-b+epsvecm/lam
            diagx = plam/ux3+qlam/xl3
            diagx = 2*diagx+xsi/(x-alfa)+eta/(beta-x)
            diagxinv = een/diagx
            diagy = d+mu/y
            diagyinv = eem/diagy
            diaglam = s/lam
            diaglamyi = diaglam+diagyinv
            # Start if m<n
            if m < n:
                blam = dellam+dely/diagy-np.dot(GG, (delx/diagx))
                bb = np.concatenate((blam, delz), axis=0)
                Alam = np.asarray(diags(diaglamyi.flatten(), 0)
                                  + (diags(diagxinv.flatten(), 0).dot(GG.T).T).dot(GG.T))
                AAr1 = np.concatenate((Alam, a), axis=1)
                AAr2 = np.concatenate((a, -zet/z), axis=0).T
                AA = np.concatenate((AAr1, AAr2), axis=0)
                solut = solve(AA, bb)
                dlam = solut[0:m]
                dz = solut[m:m+1]
                dx = -delx/diagx-np.dot(GG.T, dlam)/diagx
            else:
                diaglamyiinv = eem/diaglamyi
                dellamyi = dellam+dely/diagy
                Axx = np.asarray(diags(diagx.flatten(), 0)
                                 + (diags(diaglamyiinv.flatten(), 0).dot(GG).T).dot(GG))
                azz = zet/z+np.dot(a.T, (a/diaglamyi))
                axz = np.dot(-GG.T, (a/diaglamyi))
                bx = delx+np.dot(GG.T, (dellamyi/diaglamyi))
                bz = delz-np.dot(a.T, (dellamyi/diaglamyi))
                AAr1 = np.concatenate((Axx, axz), axis=1)
                AAr2 = np.concatenate((axz.T, azz), axis=1)
                AA = np.concatenate((AAr1, AAr2), axis=0)
                bb = np.concatenate((-bx, -bz), axis=0)
                # print(AA)
                # print(bb)
                solut = solve(AA, bb)
                dx = solut[0:n]
                dz = solut[n:n+1]
                dlam = np.dot(GG, dx)/diaglamyi-dz*(a/diaglamyi)+dellamyi/diaglamyi
                # End if m<n
            dy = -dely/diagy+dlam/diagy
            dxsi = -xsi+epsvecn/(x-alfa)-(xsi*dx)/(x-alfa)
            deta = -eta+epsvecn/(beta-x)+(eta*dx)/(beta-x)
            dmu = -mu+epsvecm/y-(mu*dy)/y
            dzet = -zet+epsi/z-zet*dz/z
            ds = -s+epsvecm/lam-(s*dlam)/lam
            xx = np.concatenate((y, z, lam, xsi, eta, mu, zet, s), axis=0)
            dxx = np.concatenate((dy, dz, dlam, dxsi, deta, dmu, dzet, ds), axis=0)
            #
            stepxx = -1.01*dxx/xx
            stmxx = np.max(stepxx)
            stepalfa = -1.01*dx/(x-alfa)
            stmalfa = np.max(stepalfa)
            stepbeta = 1.01*dx/(beta-x)
            stmbeta = np.max(stepbeta)
            stmalbe = max(stmalfa, stmbeta)
            stmalbexx = max(stmalbe, stmxx)
            stminv = max(stmalbexx, 1.0)
            steg = 1.0/stminv
            #
            xold = x.copy()
            yold = y.copy()
            zold = z.copy()
            lamold = lam.copy()
            xsiold = xsi.copy()
            etaold = eta.copy()
            muold = mu.copy()
            zetold = zet.copy()
            sold = s.copy()
            #
            itto = 0
            resinew = 2*residunorm
            # Start: while (resinew>residunorm) and (itto<50)
            while (resinew > residunorm) and (itto < 50):
                itto = itto+1
                x = xold+steg*dx
                y = yold+steg*dy
                z = zold+steg*dz
                lam = lamold+steg*dlam
                xsi = xsiold+steg*dxsi
                eta = etaold+steg*deta
                mu = muold+steg*dmu
                zet = zetold+steg*dzet
                s = sold+steg*ds
                ux1 = upp-x
                xl1 = x-low
                ux2 = ux1*ux1
                xl2 = xl1*xl1
                uxinv1 = een/ux1
                xlinv1 = een/xl1
                plam = p0+np.dot(P.T, lam)
                qlam = q0+np.dot(Q.T, lam)
                gvec = np.dot(P, uxinv1)+np.dot(Q, xlinv1)
                dpsidx = plam/ux2-qlam/xl2
                rex = dpsidx-xsi+eta
                rey = c+d*y-mu-lam
                rez = a0-zet-np.dot(a.T, lam)
                relam = gvec-np.dot(a, z)-y+s-b
                rexsi = xsi*(x-alfa)-epsvecn
                reeta = eta*(beta-x)-epsvecn
                remu = mu*y-epsvecm
                rezet = np.dot(zet, z)-epsi
                res = lam*s-epsvecm
                residu1 = np.concatenate((rex, rey, rez), axis=0)
                residu2 = np.concatenate((relam, rexsi, reeta, remu, rezet, res), axis=0)
                residu = np.concatenate((residu1, residu2), axis=0)
                resinew = np.sqrt(np.dot(residu.T, residu))
                steg = steg/2
                # End: while (resinew>residunorm) and (itto<50)
            residunorm = resinew.copy()
            residumax = max(abs(residu))
            steg = 2*steg
            # End: while (residumax>0.9*epsi) and (ittt<200)
        epsi = 0.1*epsi
        # End: while epsi>epsimin
    xmma = x.copy()
    ymma = y.copy()
    zmma = z.copy()
    lamma = lam
    xsimma = xsi
    etamma = eta
    mumma = mu
    zetmma = zet
    smma = s
    # Return values
    return xmma, ymma, zmma, lamma, xsimma, etamma, mumma, zetmma, smma

# Function for Karush–Kuhn–Tucker check


def kktcheck(m, n, x, y, z, lam, xsi, eta, mu, zet, s, xmin, xmax, df0dx, fval, dfdx, a0, a, c, d):
    """
    The left hand sides of the KKT conditions for the following nonlinear programming problem are
    calculated.

    Minimize f_0(x) + a_0*z + sum(c_i*y_i + 0.5*d_i*(y_i)^2)
    subject to  f_i(x) - a_i*z - y_i <= 0,   i = 1,...,m
                xmax_j <= x_j <= xmin_j,     j = 1,...,n
                z >= 0,   y_i >= 0,          i = 1,...,m

    INPUT:

        m     = The number of general constraints.
        n     = The number of variables x_j.
        x     = Current values of the n variables x_j.
        y     = Current values of the m variables y_i.
        z     = Current value of the single variable z.
        lam   = Lagrange multipliers for the m general constraints.
        xsi   = Lagrange multipliers for the n constraints xmin_j - x_j <= 0.
        eta   = Lagrange multipliers for the n constraints x_j - xmax_j <= 0.
        mu    = Lagrange multipliers for the m constraints -y_i <= 0.
        zet   = Lagrange multiplier for the single constraint -z <= 0.
        s     = Slack variables for the m general constraints.
        xmin  = Lower bounds for the variables x_j.
        xmax  = Upper bounds for the variables x_j.
        df0dx = Vector with the derivatives of the objective function f_0
                with respect to the variables x_j, calculated at x.
        fval  = Vector with the values of the constraint functions f_i,
                calculated at x.
        dfdx  = (m x n)-matrix with the derivatives of the constraint functions
                f_i with respect to the variables x_j, calculated at x.
                dfdx(i,j) = the derivative of f_i with respect to x_j.
        a0    = The constants a_0 in the term a_0*z.
        a     = Vector with the constants a_i in the terms a_i*z.
        c     = Vector with the constants c_i in the terms c_i*y_i.
        d     = Vector with the constants d_i in the terms 0.5*d_i*(y_i)^2.

    OUTPUT:

        residu     = the residual vector for the KKT conditions.
        residunorm = sqrt(residu'*residu).
        residumax  = max(abs(residu)).

    """

    rex = df0dx+np.dot(dfdx.T, lam)-xsi+eta
    rey = c+d*y-mu-lam
    rez = a0-zet-np.dot(a.T, lam)
    relam = fval-a*z-y+s
    rexsi = xsi*(x-xmin)
    reeta = eta*(xmax-x)
    remu = mu*y
    rezet = zet*z
    res = lam*s
    residu1 = np.concatenate((rex, rey, rez), axis=0)
    residu2 = np.concatenate((relam, rexsi, reeta, remu, rezet, res), axis=0)
    residu = np.concatenate((residu1, residu2), axis=0)
    residunorm = np.sqrt((np.dot(residu.T, residu)).item())
    residumax = np.max(np.abs(residu))
    return residu, residunorm, residumax

# Function for updating raa0 and raa


def raaupdate(xmma, xval, xmin, xmax, low, upp, f0valnew, fvalnew, f0app, fapp, raa0, raa, raa0eps, raaeps, epsimin):
    """
    Values of the parameters raa0 and raa are updated during an inner iteration.
    """

    raacofmin = 1e-12
    eeem = np.ones((raa.size, 1))
    eeen = np.ones((xmma.size, 1))
    xmami = xmax-xmin
    xmamieps = 0.00001*eeen
    xmami = np.maximum(xmami, xmamieps)
    xxux = (xmma-xval)/(upp-xmma)
    xxxl = (xmma-xval)/(xmma-low)
    xxul = xxux*xxxl
    ulxx = (upp-low)/xmami
    raacof = np.dot(xxul.T, ulxx)
    raacof = np.maximum(raacof, raacofmin)
    #
    f0appe = f0app+0.5*epsimin
    if np.all(f0valnew > f0appe) == True:
        deltaraa0 = (1.0/raacof)*(f0valnew-f0app)
        zz0 = 1.1*(raa0+deltaraa0)
        zz0 = np.minimum(zz0, 10*raa0)
        raa0 = zz0
    #
    fappe = fapp+0.5*epsimin*eeem
    fdelta = fvalnew-fappe
    deltaraa = (1/raacof)*(fvalnew-fapp)
    zzz = 1.1*(raa+deltaraa)
    zzz = np.minimum(zzz, 10*raa)
    raa[np.where(fdelta > 0)] = zzz[np.where(fdelta > 0)]
    #
    return raa0, raa

# Function to check if the approsimations are conservative


def concheck(m, epsimin, f0app, f0valnew, fapp, fvalnew):
    """
    If the current approximations are conservative, the parameter conserv is set to 1.
    """

    eeem = np.ones((m, 1))
    f0appe = f0app+epsimin
    fappe = fapp+epsimin*eeem
    arr1 = np.concatenate((f0appe.flatten(), fappe.flatten()))
    arr2 = np.concatenate((f0valnew.flatten(), fvalnew.flatten()))
    if np.all(arr1 >= arr2) == True:
        conserv = 1
    else:
        conserv = 0
    return conserv

# Calculate low, upp, raa0, raa in the beginning of each outer iteration


def asymp(outeriter, n, xval, xold1, xold2, xmin, xmax, low, upp, raa0, raa, raa0eps, raaeps, df0dx, dfdx):
    """
    Values on the parameters raa0, raa, low and upp are calculated in the beginning of each outer
    iteration.
    """

    eeen = np.ones((n, 1))
    asyinit = 0.5
    asyincr = 1.2
    asydecr = 0.7
    xmami = xmax-xmin
    xmamieps = 0.00001*eeen
    xmami = np.maximum(xmami, xmamieps)
    raa0 = np.dot(np.abs(df0dx).T, xmami)
    raa0 = np.maximum(raa0eps, (0.1/n)*raa0)
    raa = np.dot(np.abs(dfdx), xmami)
    raa = np.maximum(raaeps, (0.1/n)*raa)
    if outeriter <= 2:
        low = xval-asyinit*xmami
        upp = xval+asyinit*xmami
    else:
        xxx = (xval-xold1)*(xold1-xold2)
        factor = eeen.copy()
        factor[np.where(xxx > 0)] = asyincr
        factor[np.where(xxx < 0)] = asydecr
        low = xval-factor*(xold1-low)
        upp = xval+factor*(upp-xold1)
        lowmin = xval-10*xmami
        lowmax = xval-0.01*xmami
        uppmin = xval+0.01*xmami
        uppmax = xval+10*xmami
        low = np.maximum(low, lowmin)
        low = np.minimum(low, lowmax)
        upp = np.minimum(upp, uppmax)
        upp = np.maximum(upp, uppmin)
    return low, upp, raa0, raa


def setup_logger(logfile):
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # Create file handler and set level to debug
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    # Add formatter to ch and fh
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # Add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    # Open logfile and reset
    with open(logfile, 'w'):
        pass
    # Return logger
    return logger


# Function for the example with evaluation of f and g
def _evaluate_f_g(xval, *args):
    nx = 5
    eeen = np.ones((nx, 1))
    c1 = args[5]
    c2 = args[6]
    aaa = np.array([args[:5]]).T
    xval2 = xval*xval
    xval3 = xval2*xval
    xinv3 = eeen/xval3
    f0val = c1*np.dot(eeen.T, xval)
    fval = np.dot(aaa.T, xinv3)-c2
    return f0val, fval

# Function for the example with evaluation of f and g


def _evaluate_f_g_derivatives(xval, *args):
    nx = 5
    eeen = np.ones((nx, 1))
    c1 = args[5]
    c2 = args[6]
    aaa = np.array([args[:5]]).T
    xval2 = xval*xval
    xval3 = xval2*xval
    xval4 = xval2*xval2
    xinv3 = eeen/xval3
    xinv4 = eeen/xval4
    f0val = c1*np.dot(eeen.T, xval).item()
    df0dx = c1*eeen
    fval = np.dot(aaa.T, xinv3).item()-c2
    dfdx = -3*(aaa*xinv4).T
    return f0val, df0dx, fval, dfdx

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    """
    Example of the "beam problem" from the MMA paper of Krister Svanberg.

        minimize 0.0624*(x(1) + x(2) + x(3) + x(4) + x(5))
        subject to 61/(x(1)^3) + 37/(x(2)^3) + 19/(x(3)^3) + 7/(x(4)^3) + 1/(x(5)^3) =< 1,
                1 =< x(j) =< 10, for j=1,..,5.
    """

    # Set starting point, bounds and additional arguments for the objective and constrainnt functions
    x0 = 5 * np.ones((5, 1))
    bounds = [[1, 10]*5]
    args = (61.0, 37.0, 19.0, 7.0, 1.0, 0.0624, 1)

    # Call numpy MMA and retrieve the optimum value, optimum solution and exitflag.
    fopt, xopt, exitflag = mma_numpy(_evaluate_f_g, _evaluate_f_g_derivatives, x0, bounds, args)

    print('\nOptimum Solution for Beam problem: ')
    print(xopt)
