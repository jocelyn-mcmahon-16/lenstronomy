import numpy as np
import astrofunc.util as util


class LensParam(object):
    """
    class to handle the lens model parameter
    """
    def __init__(self, kwargs_options, kwargs_fixed):
        """

        :param kwargs_options:
        :param kwargs_fixed:
        """
        self.kwargs_options = kwargs_options
        self.model_list = kwargs_options['lens_model_list']
        self.kwargs_fixed = kwargs_fixed
        self.num_images = kwargs_options.get('num_images', 4)
        self.solver_type = kwargs_options.get('solver_type', 'NONE')

    def getParams(self, args, i):
        kwargs_list = []
        for k, model in enumerate(self.model_list):
            kwargs = {}
            kwargs_fixed = self.kwargs_fixed[k]
            if model == 'EXTERNAL_SHEAR':
                if not 'e1' in kwargs_fixed:
                    kwargs['e1'] = args[i]
                    i += 1
                else:
                    kwargs['e1'] = kwargs_fixed['e1']
                if not 'e2' in kwargs_fixed:
                    kwargs['e2'] = args[i]
                    i += 1
                else:
                    kwargs['e2'] = kwargs_fixed['e2']
            if model == 'FLEXION':
                if not 'g1' in kwargs_fixed:
                    kwargs['g1'] = args[i]
                    i += 1
                else:
                    kwargs['g1'] = kwargs_fixed['g1']
                if not 'g2' in kwargs_fixed:
                    kwargs['g2'] = args[i]
                    i += 1
                else:
                    kwargs['g2'] = kwargs_fixed['g2']
                if not 'g3' in kwargs_fixed:
                    kwargs['g3'] = args[i]
                    i += 1
                else:
                    kwargs['g3'] = kwargs_fixed['g3']
                if not 'g4' in kwargs_fixed:
                    kwargs['g4'] = args[i]
                    i += 1
                else:
                    kwargs['g4'] = kwargs_fixed['g4']
            if model == 'GAUSSIAN':
                if not 'amp' in kwargs_fixed:
                    kwargs['amp'] = args[i]
                    i += 1
                else:
                    kwargs['amp'] = kwargs_fixed['amp']
                if not 'sigma_x' in kwargs_fixed:
                    kwargs['sigma_x'] = np.exp(args[i])
                    i += 1
                else:
                    kwargs['sigma_x'] = kwargs_fixed['sigma_x']
                if not 'sigma_y' in kwargs_fixed:
                    kwargs['sigma_y'] = np.exp(args[i])
                    i += 1
                else:
                    kwargs['sigma_y'] = kwargs_fixed['sigma_y']
            if model in ['SPEP', 'SPEMD', 'SIS', 'SIS_TRUNCATED', 'SPP']:
                if not 'theta_E' in kwargs_fixed:
                    kwargs['theta_E'] = args[i]
                    i += 1
                else:
                    kwargs['theta_E'] = kwargs_fixed['theta_E']
            if model in ['SPEP', 'SPEMD', 'SPP']:
                if not 'gamma' in kwargs_fixed:
                    kwargs['gamma'] = args[i]
                    i += 1
                else:
                    kwargs['gamma'] = kwargs_fixed['gamma']
            if model in ['SPEP', 'SPEMD', 'NFW_ELLIPSE']:
                if not 'q' in kwargs_fixed or not 'phi_G' in kwargs_fixed:
                    phi, q = util.elliptisity2phi_q(args[i], args[i+1])
                    kwargs['phi_G'] = phi
                    kwargs['q'] = q
                    i += 2
                else:
                    kwargs['phi_G'] = kwargs_fixed['phi_G']
                    kwargs['q'] = kwargs_fixed['q']

            if model in ['NFW', 'NFW_ELLIPSE']:
                if not 'Rs' in kwargs_fixed:
                    kwargs['Rs'] = np.exp(args[i])
                    i += 1
                else:
                    kwargs['Rs'] = kwargs_fixed['Rs']
                if not 'theta_Rs' in kwargs_fixed:
                    kwargs['theta_Rs'] = args[i]
                    i += 1
                else:
                    kwargs['theta_Rs'] = kwargs_fixed['theta_Rs']

            if model in ['SHAPELETS_POLAR', 'SHAPELETS_CART']:
                if not 'beta' in kwargs_fixed:
                    kwargs['beta'] = args[i]
                    i += 1
                else:
                    kwargs['beta'] = kwargs_fixed['beta']
                if not 'coeffs' in kwargs_fixed:
                    num_coeffs = self.kwargs_options['num_shapelet_lens']
                    if self.solver_type == 'SHAPELETS':
                        if self.num_images == 4:
                            num_coeffs -= 6
                            coeffs = args[i:i+num_coeffs]
                            coeffs = [0,0,0,0,0,0] + list(coeffs[0:])
                        elif self.num_images == 2:
                            num_coeffs -=3
                            coeffs = args[i:i+num_coeffs]
                            coeffs = [0, 0, 0] + list(coeffs[0:])
                        else:
                            raise ValueError("Option for solver_type not valid!")
                        kwargs['coeffs'] = coeffs
                    else:
                        kwargs['coeffs'] = args[i:i+num_coeffs]
                    i += num_coeffs
                else:
                    kwargs['coeffs'] = kwargs_fixed['coeffs']

            if model in ['DIPOLE']:
                if not 'coupling' in kwargs_fixed:
                    kwargs['coupling'] = args[i]
                    i += 1
                else:
                    kwargs['coupling'] = kwargs_fixed['coupling']
                if not 'phi_dipole' in kwargs_fixed and self.kwargs_options['phi_dipole_decoupling'] is True:
                    kwargs['phi_dipole'] = args[i]
                    i += 1
                else:
                    kwargs['phi_dipole'] = kwargs_fixed['phi_dipole']
            if model in ['SERSIC']:
                if not 'n_sersic' in kwargs_fixed:
                    kwargs['n_sersic'] = args[i]
                    i += 1
                else:
                    kwargs['n_sersic'] = kwargs_fixed['n_sersic']
                if not 'r_eff' in kwargs_fixed:
                    kwargs['r_eff'] = args[i]
                    i += 1
                else:
                    kwargs['r_eff'] = kwargs_fixed['r_eff']
                if not 'k_eff' in kwargs_fixed:
                    kwargs['k_eff'] = args[i]
                    i += 1
                else:
                    kwargs['k_eff'] = kwargs_fixed['k_eff']
            if model in ['SIS', 'SPP', 'SPEP', 'SPEMD', 'NFW', 'NFW_ELLIPSE', 'SIS_TRUNCATED', 'SHAPELETS_POLAR', 'SHAPELETS_CART', 'DIPOLE', 'GAUSSIAN', 'SERSIC']:
                if not 'center_x' in kwargs_fixed:
                    kwargs['center_x'] = args[i]
                    i += 1
                else:
                    kwargs['center_x'] = kwargs_fixed['center_x']
                if not 'center_y' in kwargs_fixed:
                    kwargs['center_y'] = args[i]
                    i += 1
                else:
                    kwargs['center_y'] = kwargs_fixed['center_y']
            kwargs_list.append(kwargs)
        return kwargs_list, i

    def setParams(self, kwargs_list):
        """

        :param kwargs:
        :return:
        """
        args = []
        for k, model in enumerate(self.model_list):
            kwargs = kwargs_list[k]
            kwargs_fixed = self.kwargs_fixed[k]
            if model == 'EXTERNAL_SHEAR':
                if not 'e1' in kwargs_fixed:
                    args.append(kwargs['e1'])
                if not 'e2' in kwargs_fixed:
                    args.append(kwargs['e2'])
            if model == 'FLEXION':
                if not 'g1' in kwargs_fixed:
                    args.append(kwargs['g1'])
                if not 'g2' in kwargs_fixed:
                    args.append(kwargs['g2'])
                if not 'g3' in kwargs_fixed:
                    args.append(kwargs['g3'])
                if not 'g4' in kwargs_fixed:
                    args.append(kwargs['g4'])
            if model == 'GAUSSIAN':
                if not 'amp' in kwargs_fixed:
                    args.append(kwargs['amp'])
                if not 'sigma_x' in kwargs_fixed:
                    args.append(np.log(kwargs['sigma_x']))
                if not 'sigma_y' in kwargs_fixed:
                    args.append(np.log(kwargs['sigma_y']))

            if model in ['SPEP', 'SPEMD', 'SIS', 'SIS_TRUNCATED', 'SPP']:
                if not 'theta_E' in kwargs_fixed:
                    args.append(kwargs['theta_E'])
            if model in ['SPEP', 'SPEMD', 'SPP']:
                if not 'gamma' in kwargs_fixed:
                    args.append(kwargs['gamma'])
            if model in ['SPEP', 'SPEMD', 'NFW_ELLIPSE']:
                if not 'q' in kwargs_fixed or not 'phi_G' in kwargs_fixed:
                    e1, e2 = util.phi_q2_elliptisity(kwargs['phi_G'], kwargs['q'])
                    args.append(e1)
                    args.append(e2)

            if model in ['NFW', 'NFW_ELLIPSE']:
                if not 'Rs' in kwargs_fixed:
                    args.append(np.log(kwargs['Rs']))
                if not 'theta_Rs' in kwargs_fixed:
                    args.append(kwargs['theta_Rs'])

            if model in ['SHAPELETS_POLAR', 'SHAPELETS_CART']:
                if not 'beta' in kwargs_fixed:
                    args.append(kwargs['beta'])
                if not 'coeffs' in kwargs_fixed:
                    coeffs = kwargs['coeffs']
                    if self.solver_type == 'SHAPELETS':
                        if self.num_images == 4:
                            coeffs = coeffs[6:]
                        elif self.num_images == 2:
                            coeffs = coeffs[3:]
                    args += list(coeffs)

            if model in ['DIPOLE']:
                if not 'coupling' in kwargs_fixed:
                    args.append(kwargs['coupling'])
                if not 'phi_dipole' in kwargs_fixed and self.kwargs_options['phi_dipole_decoupling'] is True:
                    args.append(kwargs['phi_dipole'])
            if model in ['SERSIC']:
                if not 'n_sersic' in kwargs_fixed:
                    args.append(kwargs['n_sersic'])
                if not 'r_eff' in kwargs_fixed:
                    args.append(kwargs['r_eff'])
                if not 'k_eff' in kwargs_fixed:
                    args.append(kwargs['k_eff'])
            if model in ['SIS', 'SPP', 'SPEP', 'SPEMD', 'NFW', 'NFW_ELLIPSE', 'SIS_TRUNCATED', 'SHAPELETS_POLAR',
                                 'SHAPELETS_CART', 'DIPOLE', 'GAUSSIAN', 'SERSIC']:
                if not 'center_x' in kwargs_fixed:
                    args.append(kwargs['center_x'])
                if not 'center_y' in kwargs_fixed:
                    args.append(kwargs['center_y'])
        return args

    def add2fix(self, kwargs_fixed_list):
        """

        :param kwargs_fixed:
        :return:
        """
        fix_return_list = []
        for k, model in enumerate(self.model_list):
            kwargs_fixed = kwargs_fixed_list[k]
            fix_return = {}
            if model == 'EXTERNAL_SHEAR':
                if 'e1' in kwargs_fixed:
                    fix_return['e1'] = kwargs_fixed['e1']
                if 'e2' in kwargs_fixed:
                    fix_return['e2'] = kwargs_fixed['e2']
            if model == 'FLEXION':
                if 'g1' in kwargs_fixed:
                    fix_return['g1'] = kwargs_fixed['g1']
                if 'g2' in kwargs_fixed:
                    fix_return['g2'] = kwargs_fixed['g2']
                if 'g3' in kwargs_fixed:
                    fix_return['g3'] = kwargs_fixed['g3']
                if 'g4' in kwargs_fixed:
                    fix_return['g4'] = kwargs_fixed['g4']
            if model == 'GAUSSIAN':
                if 'amp' in kwargs_fixed:
                    fix_return['amp'] = kwargs_fixed['amp']
                if 'sigma_x' in kwargs_fixed:
                    fix_return['sigma_x'] = kwargs_fixed['sigma_x']
                if 'sigma_y' in kwargs_fixed:
                    fix_return['sigma_y'] = kwargs_fixed['sigma_y']

            if model in ['SPEP', 'SPEMD', 'SIS', 'SIS_TRUNCATED', 'SPP']:
                if 'theta_E' in kwargs_fixed:
                    fix_return['theta_E'] = kwargs_fixed['theta_E']
            if model in ['SPEP', 'SPEMD', 'SPP']:
                if 'gamma' in kwargs_fixed:
                    fix_return['gamma'] = kwargs_fixed['gamma']
            if model in ['SPEP', 'SPEMD', 'NFW_ELLIPSE']:
                if 'q' in kwargs_fixed and 'phi_G' in kwargs_fixed:
                    fix_return['phi_G'] = kwargs_fixed['phi_G']
                    fix_return['q'] = kwargs_fixed['q']

            if model in ['NFW', 'NFW_ELLIPSE']:
                if 'Rs' in kwargs_fixed:
                    fix_return['Rs'] = kwargs_fixed['Rs']
                if 'theta_Rs' in kwargs_fixed:
                    fix_return['theta_Rs'] = kwargs_fixed['theta_Rs']

            if model in ['SHAPELETS_POLAR', 'SHAPELETS_CART']:
                if 'beta' in kwargs_fixed:
                    fix_return['beta'] = kwargs_fixed['beta']
                if 'coeffs' in kwargs_fixed:
                    fix_return['coeffs'] = kwargs_fixed['coeffs']

            if model in ['DIPOLE']:
                if 'coupling' in kwargs_fixed:
                    fix_return['coupling'] = kwargs_fixed['coupling']
                if 'phi_dipole' in kwargs_fixed:
                    fix_return['phi_dipole'] = kwargs_fixed['phi_dipole']
            if model in ['SERSIC']:
                if 'n_sersic' in kwargs_fixed:
                    fix_return['n_sersic'] = kwargs_fixed['n_sersic']
                if 'r_eff' in kwargs_fixed:
                    fix_return['r_eff'] = kwargs_fixed['r_eff']
                if 'k_eff' in kwargs_fixed:
                    fix_return['k_eff'] = kwargs_fixed['k_eff']

            if model in ['SIS', 'SPP', 'SPEP', 'SPEMD', 'NFW', 'NFW_ELLIPSE', 'SIS_TRUNCATED', 'SHAPELETS_POLAR',
                                 'SHAPELETS_CART', 'DIPOLE', 'GAUSSIAN', 'SERSIC']:
                if 'center_x' in kwargs_fixed:
                    fix_return['center_x'] = kwargs_fixed['center_x']
                if 'center_y' in kwargs_fixed:
                    fix_return['center_y'] = kwargs_fixed['center_y']
            fix_return_list.append(fix_return)
        return fix_return_list

    def param_init(self, kwargs_mean_list):
        """

        :param kwargs_mean:
        :return:
        """
        mean = []
        sigma = []
        for k, model in enumerate(self.model_list):
            kwargs_mean = kwargs_mean_list[k]
            kwargs_fixed = self.kwargs_fixed[k]
            if model == 'EXTERNAL_SHEAR':
                if not 'e1' in kwargs_fixed:
                    mean.append(kwargs_mean['e1'])
                    sigma.append(kwargs_mean['shear_sigma'])
                if not 'e2' in kwargs_fixed:
                    mean.append(kwargs_mean['e2'])
                    sigma.append(kwargs_mean['shear_sigma'])
            if model == 'FLEXION':
                if not 'g1' in kwargs_fixed:
                    mean.append(kwargs_mean['g1'])
                    sigma.append(kwargs_mean['flexion_sigma'])
                if not 'g2' in kwargs_fixed:
                    mean.append(kwargs_mean['g2'])
                    sigma.append(kwargs_mean['flexion_sigma'])
                if not 'g3' in kwargs_fixed:
                    mean.append(kwargs_mean['g3'])
                    sigma.append(kwargs_mean['flexion_sigma'])
                if not 'g4' in kwargs_fixed:
                    mean.append(kwargs_mean['g4'])
                    sigma.append(kwargs_mean['flexion_sigma'])
            if model == 'GAUSSIAN':
                if not 'amp' in kwargs_fixed:
                    mean.append(kwargs_mean['amp'])
                    sigma.append(kwargs_mean['amp_sigma'])
                if not 'sigma_x' in kwargs_fixed:
                    mean.append(np.log(kwargs_mean['sigma_x']))
                    sigma.append(np.log(1 + kwargs_mean['sigma_x_sigma']/kwargs_mean['sigma_x']))
                if not 'sigma_y' in kwargs_fixed:
                    mean.append(np.log(kwargs_mean['sigma_y']))
                    sigma.append(np.log(1 + kwargs_mean['sigma_y_sigma']/kwargs_mean['sigma_y']))

            if model in ['SPEP', 'SPEMD', 'SIS', 'SIS_TRUNCATED', 'SPP']:
                if not 'theta_E' in kwargs_fixed:
                    mean.append(kwargs_mean['theta_E'])
                    sigma.append(kwargs_mean['theta_E_sigma'])
            if model in ['SPEP', 'SPEMD', 'SPP']:
                if not 'gamma' in \
                        kwargs_fixed:
                    mean.append(kwargs_mean['gamma'])
                    sigma.append(kwargs_mean['gamma_sigma'])
            if model in ['SPEP', 'SPEMD', 'NFW_ELLIPSE']:
                if not 'q' in kwargs_fixed or not 'phi_G' in kwargs_fixed:
                    phi = kwargs_mean['phi_G']
                    q = kwargs_mean['q']
                    e1, e2 = util.phi_q2_elliptisity(phi, q)
                    mean.append(e1)
                    mean.append(e2)
                    ellipse_sigma = kwargs_mean['ellipse_sigma']
                    sigma.append(ellipse_sigma)
                    sigma.append(ellipse_sigma)

            if model in ['NFW', 'NFW_ELLIPSE']:
                if not 'Rs' in kwargs_fixed:
                    mean.append(np.log(kwargs_mean['Rs']))
                    sigma.append(np.log(1 + kwargs_mean['Rs_sigma']/kwargs_mean['Rs']))
                if not 'theta_Rs' in kwargs_fixed:
                    mean.append(kwargs_mean['theta_Rs'])
                    sigma.append(kwargs_mean['theta_Rs_sigma'])

            if model in ['SHAPELETS_POLAR', 'SHAPELETS_CART']:
                if not 'beta' in kwargs_fixed:
                    mean.append(kwargs_mean['beta'])
                    sigma.append(kwargs_mean['beta_sigma'])
                if not 'coeffs' in kwargs_fixed:
                    coeffs = kwargs_mean['coeffs']
                    if self.solver_type == 'SHAPELETS':
                        if self.num_images == 4:
                            coeffs = coeffs[6:]
                        elif self.num_images == 2:
                            coeffs = coeffs[3:]
                    for i in range(0, len(coeffs)):
                        mean.append(coeffs[i])
                        sigma.append(kwargs_mean['coeffs_sigma'])

            if model in ['DIPOLE']:
                if not 'coupling' in kwargs_fixed:
                    mean.append(kwargs_mean['coupling'])
                    sigma.append(kwargs_mean['coupling_sigma'])
                if not 'phi_dipole' in kwargs_fixed and self.kwargs_options['phi_dipole_decoupling'] is True:
                    mean.append(kwargs_mean['phi_dipole'])
                    sigma.append(kwargs_mean['phi_dipole_sigma'])
            if model in ['SERSIC']:
                if not 'n_sersic' in kwargs_fixed:
                    mean.append(kwargs_mean['n_sersic'])
                    sigma.append(kwargs_mean['n_sersic_sigma'])
                if not 'r_eff' in kwargs_fixed:
                    mean.append(kwargs_mean['r_reff'])
                    sigma.append(kwargs_mean['r_eff_sigma'])
                if not 'k_eff' in kwargs_fixed:
                    mean.append(kwargs_mean['k_reff'])
                    sigma.append(kwargs_mean['k_eff_sigma'])
            if model in ['SIS', 'SPP', 'SPEP', 'SPEMD', 'NFW', 'NFW_ELLIPSE', 'SIS_TRUNCATED', 'SHAPELETS_POLAR', 'SHAPELETS_CART', 'DIPOLE', 'GAUSSIAN', 'SERSIC']:
                if not 'center_x' in kwargs_fixed:
                    mean.append(kwargs_mean['center_x'])
                    sigma.append(kwargs_mean['center_x_sigma'])
                if not 'center_y' in kwargs_fixed:
                    mean.append(kwargs_mean['center_y'])
                    sigma.append(kwargs_mean['center_y_sigma'])
        return mean, sigma

    def param_bounds(self):
        """

        :return:
        """
        low = []
        high = []
        for k, model in enumerate(self.model_list):
            kwargs_fixed = self.kwargs_fixed[k]
            if model == 'EXTERNAL_SHEAR':
                if not 'e1' in kwargs_fixed:
                    low.append(-0.5)
                    high.append(0.5)
                if not 'e2' in kwargs_fixed:
                    low.append(-0.5)
                    high.append(0.5)
            if model == 'FLEXION':
                if not 'g1' in kwargs_fixed:
                    low.append(-0.1)
                    high.append(0.1)
                if not 'g2' in kwargs_fixed:
                    low.append(-0.1)
                    high.append(0.1)
                if not 'g3' in kwargs_fixed:
                    low.append(-0.1)
                    high.append(0.1)
                if not 'g4' in kwargs_fixed:
                    low.append(-0.1)
                    high.append(0.1)
            if model == 'GAUSSIAN':
                if not 'amp' in kwargs_fixed:
                    low.append(0)
                    high.append(1000)
                if not 'sigma_x' in kwargs_fixed:
                    low.append(-10)
                    high.append(10)
                if not 'sigma_y' in kwargs_fixed:
                    low.append(-10)
                    high.append(10)

            if model in ['SPEP', 'SPEMD', 'SIS', 'SIS_TRUNCATED', 'SPP']:
                if not 'theta_E' in kwargs_fixed:
                    low.append(0.001)
                    high.append(10)
            if model in ['SPEP', 'SPEMD', 'SPP']:
                if not 'gamma' in kwargs_fixed:
                    low.append(1.5)
                    high.append(2.5)
            if model in ['SPEP', 'SPEMD', 'NFW_ELLIPSE']:
                if not 'q' in kwargs_fixed or not 'phi_G' in kwargs_fixed:
                    low.append(-0.5)
                    high.append(0.5)
                    low.append(-0.5)
                    high.append(0.5)

            if model in ['NFW', 'NFW_ELLIPSE']:
                if not 'Rs' in kwargs_fixed:
                    low.append(-5)
                    high.append(5)
                if not 'theta_Rs' in kwargs_fixed:
                    low.append(0)
                    high.append(100)

            if model in ['SHAPELETS_POLAR', 'SHAPELETS_CART']:
                if not 'beta' in kwargs_fixed:
                    low.append(0.1)
                    high.append(3.)
                if not 'coeffs' in kwargs_fixed:
                    num_coeffs = self.kwargs_options['num_shapelet_lens']
                    if self.solver_type == 'SHAPELETS':
                        if self.num_images == 4:
                            num_coeffs -= 6
                        elif self.num_images == 2:
                            num_coeffs -= 3
                    low += [-5]*num_coeffs
                    high += [5]*num_coeffs

            if model in ['DIPOLE']:
                if not 'coupling' in kwargs_fixed:
                    low.append(0)
                    high.append(10)
                if not 'phi_dipole' in kwargs_fixed and self.kwargs_options['phi_dipole_decoupling'] is True:
                    low.append(-np.pi)
                    high.append(+np.pi)
            if model in ['SERSIC']:
                if not 'n_sersic' in kwargs_fixed:
                    low.append(0.1)
                    high.append(8)
                if not 'r_eff' in kwargs_fixed:
                    low.append(0.0001)
                    high.append(20)
                if not 'k_eff' in kwargs_fixed:
                    low.append(0)
                    high.append(10)
            if model in ['SIS', 'SPP', 'SPEP', 'SPEMD', 'NFW', 'NFW_ELLIPSE', 'SIS_TRUNCATED', 'SHAPELETS_POLAR', 'SHAPELETS_CART', 'DIPOLE', 'GAUSSIAN', 'SERSIC']:
                if not 'center_x' in kwargs_fixed:
                    low.append(-20)
                    high.append(20)
                if not 'center_y' in kwargs_fixed:
                    low.append(-20)
                    high.append(20)
        return low, high

    def num_param(self):
        """

        :return:
        """
        num = 0
        list = []
        for k, model in enumerate(self.model_list):
            kwargs_fixed = self.kwargs_fixed[k]
            if model == 'EXTERNAL_SHEAR':
                if not 'e1' in kwargs_fixed:
                    num += 1
                    list.append('e1')
                if not 'e2' in kwargs_fixed:
                    num += 1
                    list.append('e2')
            if model == 'FLEXION':
                if not 'g1' in kwargs_fixed:
                    num += 1
                    list.append('g1')
                if not 'g2' in kwargs_fixed:
                    num += 1
                    list.append('g2')
                if not 'g3' in kwargs_fixed:
                    num += 1
                    list.append('g3')
                if not 'g4' in kwargs_fixed:
                    num += 1
                    list.append('g4')
            if model == 'GAUSSIAN':
                if not 'amp' in kwargs_fixed:
                    num += 1
                    list.append('amp_lens')
                if not 'sigma_x' in kwargs_fixed:
                    num += 1
                    list.append('sigma_x_lens')
                if not 'sigma_y' in kwargs_fixed:
                    num += 1
                    list.append('sigma_y_lens')
            if model in ['SPEP', 'SPEMD', 'SIS', 'SIS_TRUNCATED', 'SPP']:
                if not 'theta_E' in kwargs_fixed:
                    num+=1
                    list.append('theta_E')
            if model in ['SPEP', 'SPEMD', 'SPP']:
                if not 'gamma' in kwargs_fixed:
                    num += 1
                    list.append('gamma_lens')
            if model in ['SPEP', 'SPEMD', 'NFW_ELLIPSE']:
                if not 'q' in kwargs_fixed or not 'phi_G' in kwargs_fixed:
                    num += 2
                    list.append('e1_lens')
                    list.append('e2_lens')
            if model in ['NFW', 'NFW_ELLIPSE']:
                if not 'Rs' in kwargs_fixed:
                    num+=1
                    list.append('Rs_nfw')
                if not 'theta_Rs' in kwargs_fixed:
                    num+=1
                    list.append('theta_Rs_nfw')

            if model in ['SHAPELETS_POLAR', 'SHAPELETS_CART']:
                if not 'beta' in kwargs_fixed:
                    num+=1
                    list.append('beta_lens')
                if not 'coeffs' in kwargs_fixed:
                    num_coeffs = self.kwargs_options['num_shapelet_lens']
                    if self.solver_type == 'SHAPELETS':
                        if self.num_images == 4:
                            num_coeffs -= 6
                        elif self.num_images == 2:
                            num_coeffs -= 3
                    num += num_coeffs
                    list += ['coeff']*num_coeffs

            if model in ['DIPOLE']:
                if not 'coupling' in kwargs_fixed:
                    num += 1
                    list.append('coupling')
                if not 'phi_dipole' in kwargs_fixed and self.kwargs_options['phi_dipole_decoupling'] is True:
                    num += 1
                    list.append('phi_dipole')
            if model in ['SERSIC']:
                if not 'n_sersic' in kwargs_fixed:
                    num += 1
                    list.append('n_sersic_lens')
                if not 'r_eff' in kwargs_fixed:
                    num += 1
                    list.append('r_eff_lens')
                if not 'k_eff' in kwargs_fixed:
                    num += 1
                    list.append('k_eff_lens')
            if model in ['SIS', 'SPP', 'SPEP', 'SPEMD', 'NFW', 'NFW_ELLIPSE', 'SIS_TRUNCATED', 'SHAPELETS_POLAR', 'SHAPELETS_CART', 'DIPOLE', 'GAUSSIAN', 'SERSIC']:
                if not 'center_x' in kwargs_fixed:
                    num += 1
                    list.append('center_x_lens')
                if not 'center_y' in kwargs_fixed:
                    num += 1
                    list.append('center_y_lens')
        return num, list