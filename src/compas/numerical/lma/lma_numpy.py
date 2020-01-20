# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function


# __all__ = ['lma_numpy']


# def objective(qind, E, Ci, Cf, Ct, Cit, pzi, out=2):
#     q = E.dot(qind)
#     Q = diags([q.flatten()], [0])
#     Di = Cit.dot(Q).dot(Ci)
#     Df = Cit.dot(Q).dot(Cf)
#     zi = spsolve(Di, pzi - Df.dot(zf))
#     f = zi - zT
#     if out == 1:
#         return f
#     W = diags([zi.flatten()], [0])
#     J = spsolve(-D, Cit).dot(W).dot(E)
#     return f, J


# def lma_numpy(cost, x0, args=None, kmax=1000, tau=1e-6, eps1=1e-8, eps2=1e-8):
#     """Levenberg-Marquardt algorithm for solving least-squares problems.

#     Parameters
#     ----------
#     cost : callable
#         The objective or "cost" function.
#     x0 : array-like
#         Initial guess for the variables.
#     args : list, optional
#         Additional arguments to be passed to the objective function.
#     kmax : int, optional
#         The maximum number of iterations.
#         Default is `1000`.
#     tau : float, optional
#         Parameter for finding the step size in the steepest descent direction.
#         Default is `1e-6`.
#     eps1 : float, optional
#         Stopage criterion related to the maximum absolute value of the gradient.
#         Default is `1e-8`.
#     eps2 : float, optional
#         Stopage criterion related to the improvement between iterations.
#         Default is `1e-8`.

#     Returns
#     -------
#     list
#         * The optimal values for the optimization variables.
#         * The reason for stopping.
#         * The final iteration.
#         * The final gradient.

#     Notes
#     -----

#     References
#     ----------

#     Examples
#     --------
#     >>>
#     """
#     x = asarray(x0).reshape((-1, 1))
#     n = len(x)

#     f, J = cost(x, *args)

#     A = dot(J.transpose(), J)
#     a = diagonal(A)
#     g = dot(J.transpose(), f)

#     k = 0
#     v = 2
#     mu = tau * max(a)

#     stop = 'max(abs(g)): %s > %s' % (max(abs(g)), eps1)

#     while max(abs(g)) > eps1 :
#         dx = solve(-(A + mu * eye(n)), g)
#         xn = x + dx

#         # should the gain be calculated based on dq rather than dqind?

#         # differences between iterations become too small
#         # this means that we are at a local minimum, i think
#         if norm(dx) <= eps2 * norm(xn) :
#             stop = 'differences: %s <= %s' % (norm(dx), eps2 * norm(xn))
#             break

#         fn = cost(xn, *args, out=1)

#         # gain ratio
#         # assess whether to switch between ...
#         gain = (0.5 * (sum(power(f, 2)) - sum(power(fn, 2)))) / (0.5 * dx.transpose() * (mu * dx - g))

#         if gain > 0 :
#             x = xn

#             f, J = cost(x, *args, out=2)

#             A = dot(J.transpose(), J)
#             a = diagonal(A)
#             g = dot(J.transpose(), f)

#             mu = mu * max([1/3, 1 - (2 * gain - 1)**3])
#             v = 2

#         else :
#             mu = mu * v
#             v = 2 * v

#         k = k + 1
#         if k >= kmax :
#             stop = 'kmax'
#             break

#     return [x, stop, k, g]


# # ==============================================================================
# # Main
# # ==============================================================================

# if __name__ == "__main__":
#     pass
