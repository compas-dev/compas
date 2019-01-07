%---------------------------------------------------------------------
%  This is the file raaupdate.m.  Version April 2007.
%  Written by Krister Svanberg <krille@math.kth.se>.
%
%  Values of the parameters raa0 and raa are updated
%  during an inner iteration.
%
function [raa0,raa] = ...
raaupdate(xmma,xval,xmin,xmax,low,upp,f0valnew,fvalnew, ...
          f0app,fapp,raa0,raa,raa0eps,raaeps,epsimin);
%
raacofmin = 10^(-12);
eeem = ones(size(raa));
eeen = ones(size(xmma));
xmami = xmax-xmin;
xmamieps = 0.00001*eeen;
xmami = max(xmami,xmamieps);
xxux = (xmma-xval)./(upp-xmma);
xxxl = (xmma-xval)./(xmma-low);
xxul = xxux.*xxxl;
ulxx = (upp-low)./xmami;
raacof = xxul'*ulxx;
raacof = max(raacof,raacofmin);
%
f0appe = f0app + 0.5*epsimin;
if f0valnew > f0appe
  deltaraa0 = (1/raacof)*(f0valnew-f0app);
  zz0 = 1.1*(raa0 + deltaraa0);
  zz0 = min(zz0,10*raa0);
%  zz0 = min(zz0,1000*raa0);
  raa0 = zz0;
end
%
fappe = fapp + 0.5*epsimin*eeem;
fdelta = fvalnew-fappe;
deltaraa = (1/raacof)*(fvalnew-fapp);
zzz = 1.1*(raa + deltaraa);
zzz = min(zzz,10*raa);
%zzz = min(zzz,1000*raa);
raa(find(fdelta > 0)) = zzz(find(fdelta > 0));
%---------------------------------------------------------------------

