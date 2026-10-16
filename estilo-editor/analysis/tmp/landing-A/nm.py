import numpy as np
def nelder_mead(f, x0, step=None, iters=4000, tol=1e-10):
    x0 = np.array(x0, float); n = len(x0)
    step = np.array(step if step is not None else np.maximum(np.abs(x0)*0.1, 0.05))
    S = [x0] + [x0 + np.eye(n)[i]*step[i] for i in range(n)]
    V = [f(s) for s in S]
    for _ in range(iters):
        o = np.argsort(V); S = [S[i] for i in o]; V = [V[i] for i in o]
        if abs(V[-1] - V[0]) < tol: break
        c = np.mean(S[:-1], axis=0)
        r = c + (c - S[-1]); fr = f(r)
        if fr < V[0]:
            e = c + 2*(c - S[-1]); fe = f(e)
            if fe < fr: S[-1], V[-1] = e, fe
            else: S[-1], V[-1] = r, fr
        elif fr < V[-2]:
            S[-1], V[-1] = r, fr
        else:
            k = c + 0.5*(S[-1] - c); fk = f(k)
            if fk < V[-1]: S[-1], V[-1] = k, fk
            else:
                S = [S[0]] + [S[0] + 0.5*(s - S[0]) for s in S[1:]]
                V = [V[0]] + [f(s) for s in S[1:]]
    o = np.argmin(V)
    return S[o], V[o]
