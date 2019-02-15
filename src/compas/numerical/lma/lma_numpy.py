from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = ['lma_numpy']


def lma_numpy():
    raise NotImplementedError

    # qind0 = mat(qind0).T
    # q = EEE * qind0

    # Q = diag(q.flat)
    # D = Ci.T * Q * Ci
    # Df = Ci.T * Q * Cf
    # zi = solve(D, pz - Df * zf)

    # W = diag((Ci*zi).flat)
    # J = solve(-D, Ci.T) * W * EEE
    # A = J.T * J
    # a = diag(A)
    # f = zi - zT
    # g = J.T * f

    # tau = 1e-06
    # eps1 = 1e-08
    # eps2 = 1e-08
    # kmax = 1000
    # k = 0
    # v = 2
    # mu = tau * max(a)

    # stop = 'max(abs(g)): %s > %s' % (max(abs(g)), eps1)
    # while max(abs(g)) > eps1 :
    #     dqind = solve(-(A + mu * eye(dof)), g)
    #     dq = EEE * dqind
    #     # differences between iterations become too small
    #     # this means that we are at a local minimum, i think
    #     if norm(dq) <= eps2 * norm(q) :
    #         stop = 'differences: %s <= %s' % (norm(dq),eps2*norm(q))
    #         break
    #     qn = q + dq
    #     # linear force density
    #     Q = diag(qn.flat)
    #     D = Ci.T * Q * Ci
    #     Df = Ci.T * Q * Cf
    #     zi = solve(D, pz - Df * zf)
    #     # current difference
    #     fn = zi - zT
    #     # gain ratio
    #     # assess whether to switch between ...
    #     gain = (0.5 * (sum(power(f,2)) - sum(power(fn,2)))) / (0.5 * dqind.T * (mu * dqind - g))
    #     if gain > 0 :
    #         # ...
    #         q = qn
    #         Q = diag(q.flat)
    #         D = Ci.T * Q * Ci
    #         Df = Ci.T * Q * Cf
    #         zi = solve(D, pz - Df * zf)

    #         W = diag((Ci*zi).flat)
    #         J = solve(-D, Ci.T) * W * EEE
    #         A = J.T * J
    #         a = diag(A)
    #         f = zi - zT
    #         g = J.T * f

    #         mu = mu * max([1/3,1-(2*gain-1)**3])
    #         v = 2
    #     else :
    #         # ...
    #         mu = mu * v
    #         v = 2 * v
    #     k = k + 1
    #     if k >= kmax :
    #         stop = 'kmax'
    #         break
    # return [q, stop, k, g]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
