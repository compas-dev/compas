#include <iostream>
#include <igl/slice.h>
#include <Eigen/Dense>

extern "C" 
{
	typedef void callback(int k);

	void fd(int numv, int nume, int numfix, double** vertices, int** edges, double** loads, double* q, int* fixed, int* free);
}

void fd(int numv, int nume, int numfix, double** vertices, int** edges, double** loads, double* q, int* fixed, int* free)
{
	int i;
	int numfree = numv - numfix;

	Eigen::MatrixXd X(numv, 3);
	Eigen::MatrixXd Q = Eigen::MatrixXd::Zero(nume, nume);
	Eigen::MatrixXd C = Eigen::MatrixXd::Zero(nume, numv);

	Eigen::MatrixXd P(numv, 3);

	Eigen::MatrixXd Xi(numfree, 3);
	Eigen::MatrixXd Xf(numfix, 3);
	Eigen::MatrixXd Pi(numfree, 3);
	Eigen::MatrixXd Pf(numfix, 3);

	Eigen::MatrixXd Ci(nume, numfree);
	Eigen::MatrixXd Cit(numfree, nume);
	Eigen::MatrixXd Cf(nume, numfix);

	Eigen::VectorXi fixed_vertices(numfix);
	Eigen::VectorXi free_vertices(numfree);

	Eigen::Vector3i cols(0, 1, 2);
	Eigen::VectorXi rows = Eigen::VectorXi::LinSpaced(nume, 0, nume - 1);

	Eigen::MatrixXd A(numfree, numfree);
	Eigen::MatrixXd b(numfree, 3);

	
	for (i = 0; i < numfree; i++) {
		free_vertices(i) = free[i];
	}

	for (i = 0; i < numfix; i++) {
		fixed_vertices(i) = fixed[i];
	}

	for (i = 0; i < nume; i++) {
		C(i, edges[i][0]) = -1;
		C(i, edges[i][1]) = +1;
		Q(i, i) = q[i];
	}

	for (i = 0; i < numv; i++) {
		X(i, 0) = vertices[i][0];
		X(i, 1) = vertices[i][1];
		X(i, 2) = vertices[i][2];
		P(i, 0) = loads[i][0];
		P(i, 1) = loads[i][1];
		P(i, 2) = loads[i][2];
	}

	igl::slice(P, free_vertices, cols, Pi);
	igl::slice(X, fixed_vertices, cols, Xf);
	igl::slice(P, fixed_vertices, cols, Pf);
	igl::slice(C, rows, free_vertices, Ci);
	igl::slice(C, rows, fixed_vertices, Cf);

	Cit = Ci.transpose();

	A.noalias() = Cit * Q * Ci;
	b.noalias() = Pi - Cit * Q * Cf * Xf;

	Xi = A.colPivHouseholderQr().solve(b);

	// std::cout << Ci << '\n';
	// std::cout << A << '\n';
	// std::cout << b << '\n';
	// std::cout << Xi << '\n';

	for (i = 0; i < numfree; i++) {
		vertices[free[i]][0] = Xi(i, 0);
		vertices[free[i]][1] = Xi(i, 1);
		vertices[free[i]][2] = Xi(i, 2);
	}

}
