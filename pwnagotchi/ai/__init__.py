import os
import time
import logging


def _translate_params(params):
    supported = dict(params)
    for deprecated in ('alpha', 'epsilon', 'lr_schedule'):
        if deprecated in supported:
            logging.debug("[ai] dropping legacy parameter '%s'", deprecated)
            supported.pop(deprecated, None)

    supported.setdefault('device', 'auto')
    supported.setdefault('batch_size', 64)
    supported.setdefault('n_epochs', 4)
    supported.setdefault('gae_lambda', 0.95)
    supported.setdefault('clip_range', 0.2)
    return supported


def load(config, agent, epoch, from_disk=True):
    config = config['ai']
    if not config['enabled']:
        logging.info("ai disabled")
        return False

    try:
        begin = time.time()

        logging.info("[ai] bootstrapping dependencies ...")

        start = time.time()
        from sb3_contrib import RecurrentPPO
        logging.debug("[ai] RecurrentPPO imported in %.2fs" % (time.time() - start))

        start = time.time()
        from sb3_contrib.ppo_recurrent.policies import MlpLstmPolicy
        logging.debug("[ai] MlpLstmPolicy imported in %.2fs" % (time.time() - start))

        start = time.time()
        from stable_baselines3.common.vec_env import DummyVecEnv
        logging.debug("[ai] DummyVecEnv imported in %.2fs" % (time.time() - start))

        start = time.time()
        import pwnagotchi.ai.gym as wrappers
        logging.debug("[ai] gym wrapper imported in %.2fs" % (time.time() - start))

        base_env = wrappers.Environment(agent, epoch)
        env = DummyVecEnv([lambda: base_env])

        params = _translate_params(config['params'])
        policy_kwargs = dict(config.get('policy', {}))

        logging.info("[ai] creating model ...")

        start = time.time()
        model = RecurrentPPO(MlpLstmPolicy, env, policy_kwargs=policy_kwargs, **params)
        logging.debug("[ai] RecurrentPPO created in %.2fs" % (time.time() - start))

        if from_disk and os.path.exists(config['path']):
            logging.info("[ai] loading %s ..." % config['path'])
            start = time.time()
            model = RecurrentPPO.load(config['path'], env=env, device=params.get('device', 'auto'))
            model.set_env(env)
            logging.debug("[ai] model loaded in %.2fs" % (time.time() - start))
        else:
            logging.info("[ai] model created with parameters:")
            for key, value in params.items():
                logging.info("      %s: %s" % (key, value))
            if policy_kwargs:
                logging.info("[ai] policy overrides:")
                for key, value in policy_kwargs.items():
                    logging.info("      %s: %s" % (key, value))

        logging.debug("[ai] total loading time is %.2fs" % (time.time() - begin))

        return model
    except Exception as e:
        logging.exception("error while starting AI (%s)", e)

    logging.warning("[ai] AI not loaded!")
    return False
