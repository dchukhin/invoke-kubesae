import os

import invoke


@invoke.task
def install_requirements(c):
    """Install ansible-galaxy requirements.yml

    Usage: inv ansible.install
    """
    req_file = "requirements.yml" if os.path.exists("deploy/requirements.yml") else "requirements.yaml"
    with c.cd("deploy/"):
        c.run(f"ansible-galaxy install -f -r '{req_file}' -p roles/")


@invoke.task(pre=[install_requirements], default=True)
def ansible_deploy(c, env=None, tag=None):
    """Deploy K8s application.

    Params:
        env: The target ansible host ("staging", "production", etc ...)
        tag: The image tag in the registry to deploy

    Usage: inv deploy --env=<ENVIRONMENT> --tag=<TAG>
    """
    if env is None:
        env = c.config.env
    if tag is None:
        tag = c.config.tag
    playbook = "deploy.yaml" if os.path.exists("deploy/deploy.yaml") else "deploy.yml"
    with c.cd("deploy/"):
        c.run(f"ansible-playbook {playbook} -l {env} -e k8s_container_image_tag={tag} -vv")


deploy = invoke.Collection("deploy")
deploy.add_task(install_requirements, "install")
deploy.add_task(ansible_deploy, "deploy")
