%---------------------------------------------------------------------
%  This is the file gcmmasub.m.  Version Feb 2008.
%  Written by Krister Svanberg <krille@math.kth.se>.
%
function [xmma,ymma,zmma,lam,xsi,eta,mu,zet,s,f0app,fapp] = ...
gcmmasub(m,n,iter,epsimin,xval,xmin,xmax,low,upp, ...
         raa0,raa,f0val,df0dx,fval,dfdx,a0,a,c,d);
%
eeen = ones(n,1);
zeron = zeros(n,1);
%
% Calculations of the bounds alfa and beta.
%
albefa = 0.1;
zzz = low + albefa*(xval-low);
alfa = max(zzz,xmin);
zzz = upp - albefa*(upp-xval);
beta = min(zzz,xmax);
%
% Calculations of p0, q0, r0, P, Q, r and b.
xmami = xmax-xmin;
xmamieps = 0.00001*eeen;
xmami = max(xmami,xmamieps);
xmamiinv = eeen./xmami;
ux1 = upp-xval;
ux2 = ux1.*ux1;
xl1 = xval-low;
xl2 = xl1.*xl1;
uxinv = eeen./ux1;
xlinv = eeen./xl1;
%
p0 = zeron;
q0 = zeron;
p0 = max(df0dx,0);
q0 = max(-df0dx,0);
%p0(find(df0dx > 0)) = df0dx(find(df0dx > 0));
%q0(find(df0dx < 0)) = -df0dx(find(df0dx < 0));
pq0 = p0 + q0;
p0 = p0 + 0.001*pq0;
q0 = q0 + 0.001*pq0;
p0 = p0 + raa0*xmamiinv;
q0 = q0 + raa0*xmamiinv;
p0 = p0.*ux2;
q0 = q0.*xl2;
r0 = f0val - p0'*uxinv - q0'*xlinv;
%
P = sparse(m,n);
Q = sparse(m,n);
P = max(dfdx,0);
Q = max(-dfdx,0);
%P(find(dfdx > 0)) = dfdx(find(dfdx > 0));
%Q(find(dfdx < 0)) = -dfdx(find(dfdx < 0));
PQ = P + Q;
P = P + 0.001*PQ;
Q = Q + 0.001*PQ;
P = P + raa*xmamiinv';
Q = Q + raa*xmamiinv';
P = P * spdiags(ux2,0,n,n);
Q = Q * spdiags(xl2,0,n,n);
r = fval - P*uxinv - Q*xlinv;
b = -r;
%
% Solving the subproblem by a primal-dual Newton method
[xmma,ymma,zmma,lam,xsi,eta,mu,zet,s] = ...
subsolv(m,n,epsimin,low,upp,alfa,beta,p0,q0,P,Q,a0,a,b,c,d);
%
% Calculations of f0app and fapp.
ux1 = upp-xmma;
xl1 = xmma-low;
uxinv = eeen./ux1;
xlinv = eeen./xl1;
f0app = r0 + p0'*uxinv + q0'*xlinv;
fapp  =  r +   P*uxinv +   Q*xlinv;
%
%---------------------------------------------------------------------
