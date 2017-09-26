%---------------------------------------------------------------------
%  This is the file gcbeam.m.   Version July 2007.
%  Written by Krister Svanberg <krille@math.kth.se>.
%
%  This file contains a main program for using GCMMA to solve
%  a problem defined by the users files gcbeaminit.m
%  (which must be run before gcbeam.m), beam1.m and beam2.m.
%
%%%% If outeriter=0, the user should now calculate function values
%%%% and gradients of the objective- and constraint functions at xval.
%%%% The results should be put in f0val, df0dx, fval and dfdx:
if outeriter < 0.5
  [f0val,df0dx,fval,dfdx] = beam2(xval);
  innerit=0;
  outvector1 = [outeriter innerit f0val fval']
  outvector2 = xval'
end

%%%% The outer iterations start:
kktnorm = kkttol+10;
outit = 0;
while kktnorm > kkttol & outit < maxoutit
  outit   = outit+1;
  outeriter = outeriter+1;
%%%% The parameters low, upp, raa0 and raa are calculated:
  [low,upp,raa0,raa] = ...
  asymp(outeriter,n,xval,xold1,xold2,xmin,xmax,low,upp, ...
        raa0,raa,raa0eps,raaeps,df0dx,dfdx);
%%%% The GCMMA subproblem is solved at the point xval:
  [xmma,ymma,zmma,lam,xsi,eta,mu,zet,s,f0app,fapp] = ...
  gcmmasub(m,n,outeriter,epsimin,xval,xmin,xmax,low,upp, ...
           raa0,raa,f0val,df0dx,fval,dfdx,a0,a,c,d);
%%%% The user should now calculate function values (no gradients)
%%%% of the objective- and constraint functions at the point xmma
%%%% ( = the optimal solution of the subproblem).
%%%% The results should be put in f0valnew and fvalnew.
  [f0valnew,fvalnew] = beam1(xmma);
%%%% It is checked if the approximations are conservative:
  [conserv] = concheck(m,epsimin,f0app,f0valnew,fapp,fvalnew);
%%%% While the approximations are non-conservative (conserv=0),
%%%% repeated inner iterations are made:
  innerit=0;
  if conserv == 0
    while conserv == 0 & innerit <= 15
      innerit = innerit+1;
%%%% New values on the parameters raa0 and raa are calculated:
      [raa0,raa] = ...
      raaupdate(xmma,xval,xmin,xmax,low,upp,f0valnew,fvalnew, ...
                f0app,fapp,raa0,raa,raa0eps,raaeps,epsimin);
%%%% The GCMMA subproblem is solved with these new raa0 and raa:
      [xmma,ymma,zmma,lam,xsi,eta,mu,zet,s,f0app,fapp] = ...
      gcmmasub(m,n,outeriter,epsimin,xval,xmin,xmax,low,upp, ...
               raa0,raa,f0val,df0dx,fval,dfdx,a0,a,c,d);
%%%% The user should now calculate function values (no gradients)
%%%% of the objective- and constraint functions at the point xmma
%%%% ( = the optimal solution of the subproblem).
%%%% The results should be put in f0valnew and fvalnew:
      [f0valnew,fvalnew] = beam1(xmma);
%%%% It is checked if the approximations have become conservative:
      [conserv] = concheck(m,epsimin,f0app,f0valnew,fapp,fvalnew);
    end
  end
%%%% No more inner iterations. Some vectors are updated:
  xold2 = xold1;
  xold1 = xval;
  xval  = xmma;
%%%% The user should now calculate function values and gradients
%%%% of the objective- and constraint functions at xval.
%%%% The results should be put in f0val, df0dx, fval and dfdx:
  [f0val,df0dx,fval,dfdx] = beam2(xval);
%%%% The residual vector of the KKT conditions is calculated:
  [residu,kktnorm,residumax] = ...
  kktcheck(m,n,xmma,ymma,zmma,lam,xsi,eta,mu,zet,s, ...
           xmin,xmax,df0dx,fval,dfdx,a0,a,c,d);
  outvector1 = [outeriter innerit f0val fval']
  outvector2 = xval'
end
%---------------------------------------------------------------------

