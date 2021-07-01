import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats as stats
import scipy.linalg as linalg
import matplotlib.pyplot as plt

from scipy.optimize import minimize
from scipy.stats import norm

# stats
import statsmodels.api as sm
from statsmodels.base.model import GenericLikelihoodModel


# TODO 1: Get NashLogit working..

class NashLogit(GenericLikelihoodModel):
    
    def nloglikeobs(self, params):
        n = self.exog.shape[0]
        k = int(self.exog.shape[1]/2)
        p = np.zeros((2, 2, n))

        for a_j in [0, 1]:
            util1 = np.dot(self.exog[:, 0:k], params[0:k]) + params[-2]*a_j
            util2 = np.dot(self.exog[:, k:2*k],params[k:2*k]) + params[-1]*a_j
            p[0, a_j, :] = 1 / (1 + np.exp(util1))
            p[1, a_j, :] = 1 / (1 + np.exp(util2))
        
        #choose lambda
        lamb = .5
        delta_pos = 1*(params[-1] >= 0)*(params[-2] >= 0)
        delta_neg = 1*(params[-1] <= 0)*(params[-2] <= 0)

        if (delta_pos == 0) and (delta_neg == 0):
            params[-1] = 0
        #constrain delta2 to be pos...
        
        # solve for probablity of nash
        mult_eq = (p[0, 1, :] - p[0, 0, :])* (p[1, 1, :] - p[1, 0, :])
        prob01 = (p[0, 1, :])*(1 - p[1, 0, :]) - delta_neg*(1-lamb)*mult_eq
        
        prob10 = (1 - p[0, 0, :])*(p[1, 1, :]) - delta_neg*(lamb)*mult_eq
        prob00 = p[0, 0, :] * p[1, 0, :] - delta_pos*(1-lamb)*mult_eq
        prob11 = (1 - p[0, 1, :])*(1 - p[1, 1, :]) - delta_pos*(lamb)*mult_eq

        # compute empirical likelihood
        p00 = (1 - self.endog[:, 0])*(1 - self.endog[:, 1])
        p11 = self.endog[:, 0]*self.endog[:, 1]
        p10 = self.endog[:, 0] * (1 - self.endog[:, 1])
        p01 = (1 - self.endog[:, 0]) * self.endog[:, 1]

        ll = p00 * prob00 + p11 * prob11 + p01 * prob01 + p10 * prob10
        
        return -np.log(np.maximum(ll, 1e-12))
        

    def fit(self, **kwds):
        """fit the likelihood function using the right start parameters"""
        k = int(self.exog.shape[1]/2)
        x1 = np.concatenate( (self.exog[:, 0:k], self.endog[:,1].reshape(self.endog.shape[0],1) ) ,axis=1)
        x2 = np.concatenate( (self.exog[:, k:2*k], self.endog[:,0].reshape(self.endog.shape[0],1) ),axis=1)
        params1 =  sm.Logit(self.endog[:, 0], x1).fit().params
        params2 = sm.Logit(self.endog[:, 1], x2).fit().params
        start_params = np.concatenate((params1[0:-1],params2[0:-1],[params1[-1],params2[-1]] ))
        print(start_params)
        return super(NashLogit, self).fit(start_params=start_params, **kwds)



# TODO 2: Get BayesNashLogit working

def contraction(params, x, p):
    # beta and x are kind of parameters. x is the empirical distribution of x?
    k = int(x.shape[1]/2)
    util1 = np.dot(x[:, 0:k], params[0:k]) + params[-2]*p[:,1]
    util2 = np.dot(x[:, k:2*k], params[k:2*k]) + params[-1]*p[:,0]
    contr_result = [np.exp(util1)/(1+np.exp(util1)),
                    np.exp(util2)/(1+np.exp(util2))]
    return np.array(contr_result).transpose()


def contraction_map(betas, x, p):
    """final result is beliefs of firm1/firm2"""
    for i in range(30):
        p = contraction(betas, x, p)
    return p

class BayesNashLogit(GenericLikelihoodModel):

    def nloglikeobs(self, params):
        n = self.exog.shape[0]
        k = int(self.exog.shape[1]/2)

        p = self.endog
        p = contraction_map(params, self.exog, p)

        likelihood = contraction(params, self.exog, p)
        ll = self.endog*np.log(likelihood) + \
            (1-self.endog)*np.log(1-likelihood)
        return -1*ll.sum(axis=1)

    
    def fit(self, **kwds):
        """fit the likelihood function using the right start parameters"""
        k = int(self.exog.shape[1]/2)
        x1 = np.concatenate( (self.exog[:, 0:k], self.endog[:,1].reshape(self.endog.shape[0],1) ) ,axis=1)
        x2 = np.concatenate( (self.exog[:, k:2*k], self.endog[:,0].reshape(self.endog.shape[0],1) ),axis=1)
        params1 =  sm.Logit(self.endog[:, 0], x1).fit().params
        params2 = sm.Logit(self.endog[:, 1], x2).fit().params
        start_params = np.concatenate((params1[0:-1],params2[0:-1],[params1[-1],params2[-1]] ))
        print(start_params)
        return super(BayesNashLogit, self).fit(start_params=start_params, **kwds)


# TODO 3: Get LLR test classic version working

def setup_test(yn, xn):
    model1 = NashLogit(yn, xn)
    model1_fit = model1.fit(disp=False)
    ll1 = model1.loglikeobs(model1_fit.params)
    grad1 = model1.score_obs(model1_fit.params)
    hess1 = model1.hessian(model1_fit.params)
    params1 = model1_fit.params

    model2 = BayesNashLogit(yn, xn)
    model2_fit = model2.fit(disp=False)
    ll2 = model2.loglikeobs(model2_fit.params)
    grad2 = model2.score_obs(model2_fit.params)
    hess2 = model2.hessian(model2_fit.params)
    params2 = model2_fit.params

    return ll1, grad1, hess1, params1, ll2, grad2, hess2, params2


def regular_test(yn, xn, setup_test):
    ll1, grad1, hess1, params1, ll2, grad2, hess2, params2 = setup_test(yn, xn)
    nobs = ll1.shape[0]
    llr = (ll1 - ll2).sum()
    omega = np.sqrt((ll1 - ll2).var())
    test_stat = llr/(omega*np.sqrt(nobs))
    return 1*(test_stat >= 1.96) + 2*(test_stat <= -1.96)


# helper functions for bootstrap

def compute_eigen2(ll1,grad1,hess1,params1,ll2,grad2,hess2,params2):
    
    n = ll1.shape[0]
    hess1 = hess1/n
    hess2 = hess2/n

    k1 = params1.shape[0]
    k2 = params2.shape[0]
    k = k1 + k2
    
    #A_hat:
    A_hat1 = np.concatenate([hess1,np.zeros((k2,k1))])
    A_hat2 = np.concatenate([np.zeros((k1,k2)),-1*hess2])
    A_hat = np.concatenate([A_hat1,A_hat2],axis=1)

    #B_hat, covariance of the score...
    B_hat =  np.concatenate([grad1,-grad2],axis=1) #might be a mistake here..
    B_hat = np.cov(B_hat.transpose())

    #compute eigenvalues for weighted chisq
    sqrt_B_hat= linalg.sqrtm(B_hat)
    W_hat = np.matmul(sqrt_B_hat,linalg.inv(A_hat))
    W_hat = np.matmul(W_hat,sqrt_B_hat)
    V,W = np.linalg.eig(W_hat)

    return V



def bootstrap_distr(ll1, grad1, hess1, params1, ll2, grad2, hess2, params2, c=0, trials=500):
    nobs = ll1.shape[0]

    test_stats = []
    variance_stats = []
    llr = ll1-ll2

    for i in range(trials):
        np.random.seed()
        sample = np.random.choice(np.arange(0, nobs), nobs, replace=True)
        llrs = llr[sample]
        test_stats.append(llrs.sum())
        variance_stats.append(llrs.var())

    # final product, bootstrap
    V = compute_eigen2(ll1, grad1, hess1, params1, ll2, grad2, hess2, params2)
    test_stats = np.array(test_stats + V.sum()/(2))
    variance_stats = np.sqrt(np.array(variance_stats)*nobs + c*(V*V).sum())

    # set up test stat
    omega = np.sqrt((ll1 - ll2).var()*nobs + c*(V*V).sum())
    llr = (ll1 - ll2).sum() + V.sum()/(2)

    return test_stats, variance_stats, llr, omega

# TODO 4: Get Bootstrap test working


def bootstrap_test(yn, xn, setup_test, c=0, trials=500):
    ll1, grad1, hess1, params1, ll2, grad2, hess2, params2 = setup_test(yn, xn)

    # set up bootstrap distr
    test_stats, variance_stats, llr, omega = bootstrap_distr(
        ll1, grad1, hess1, params1, ll2, grad2, hess2, params2, c=c, trials=trials)
    test_stats = test_stats/variance_stats

    # set up confidence intervals
    cv_lower = np.percentile(test_stats, 2.5, axis=0)
    cv_upper = np.percentile(test_stats, 97.5, axis=0)

    return 2*(0 >= cv_upper) + 1*(0 <= cv_lower)
