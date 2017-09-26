%---------------------------------------------------------------------
%  This is the file concheck.m.  Version April 2007.
%  Written by Krister Svanberg <krille@math.kth.se>.
%
%  If the current approximations are conservative,
%  the parameter conserv is set to 1.
%
function [conserv] = ...
concheck(m,epsimin,f0app,f0valnew,fapp,fvalnew);
%
conserv = 0;
eeem   = ones(m,1);
f0appe = f0app+epsimin;
fappe = fapp+epsimin*eeem;
if [f0appe,fappe'] >= [f0valnew,fvalnew']
  conserv = 1;
end
%---------------------------------------------------------------------

