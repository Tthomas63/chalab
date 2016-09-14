from os import path
from zipfile import ZipFile

import pytest

from bundler import models
from bundler import tasks
from tests.bundler.tools import has, zip, remove_logo, create_bundle, bundle

pytestmark = pytest.mark.django_db

DEFAULT_DOCS = {'overview.html', 'evaluation.html', 'data.html', 'terms_and_conditions.html'}


class TestCreateBundle(object):
    def test_adds_yaml(self, challenge_ready):
        with create_bundle(challenge_ready) as (output_path, yaml, ls):
            assert 'competition.yaml' in ls

    def test_adds_documentations(self, challenge_ready):
        with create_bundle(challenge_ready) as (output_path, yaml, ls):
            assert set([x for x in ls if x.endswith('.html')]) == DEFAULT_DOCS

    def test_preserve_yaml_title(self, challenge_ready):
        with create_bundle(challenge_ready) as (output_path, yaml, ls):
            assert yaml['title'] == challenge_ready.challenge.title

    def test_adds_dataset(self, challenge_ready):
        with create_bundle(challenge_ready) as (output_path, yaml, ls):
            assert has(yaml, ['phases', 1, 'datasets', 1])

    def test_adds_logo(self, challenge_ready):
        with create_bundle(challenge_ready) as (output_path, yaml, ls):
            assert 'logo' in yaml
            assert yaml['logo'] in ls

    def test_no_logo_works(self, challenge_ready):
        remove_logo(challenge_ready)

        with create_bundle(challenge_ready) as (output_path, yaml, ls):
            assert 'logo' not in yaml

    @pytest.mark.skip
    def test_adds_reference_data(self, challenge_ready):
        c = challenge_ready.challenge

        with create_bundle(c) as (output_path, yaml, ls):
            name = has(yaml, ['phases', 1, 'datasets', 1, 'reference_data'], get_value=True)
            assert name in ls

            with zip(path.join(output_path, name)) as (z, ls):
                assert 'answer.txt' in ls
                assert 'metadata' in ls


def test_create_archive_creates_zip_file(challenge_ready):
    c = challenge_ready.challenge

    with tasks.tmp_dirs(c) as (data, output):
        tasks.create_bundle(data, c)
        a = tasks.create_archive(data, output)
        assert path.exists(a)


def log_file(bt):
    return '\n'.join([x.message for x in bt.logs])


class TestBundler(object):
    def test_set_output_zipfile(self, challenge_ready):
        with bundle(challenge_ready) as (bt, output):
            with zip(output.path) as (z, ls):
                assert 'competition.yaml' in ls

    def test_set_finished_state(self, challenge_ready):
        with bundle(challenge_ready) as (bt, output):
            assert bt.state == models.BundleTaskModel.FINISHED

    def test_bundler_stores_logs_along_the_way(self, challenge_ready):
        with bundle(challenge_ready) as (bt, output):
            lf = log_file(bt)

            assert 'Set state to finished' in lf
            assert 'Create phase 1' in lf

    def test_set_canceled_state_on_exception(self, monkeypatch, challenge_ready):
        def fail(*args, **kwargs):
            raise Exception()

        monkeypatch.setattr(tasks, 'gen_phases', fail)

        with bundle(challenge_ready) as (bt, output):
            assert bt.state == models.BundleTaskModel.FAILED

    def test_bundler_stores_logs_on_failure(self, monkeypatch, challenge_ready):
        def fail(*args, **kwargs):
            raise Exception('some random exception happened')

        monkeypatch.setattr(tasks, 'gen_phases', fail)

        with bundle(challenge_ready) as (bt, output):
            assert 'some random exception happened' in log_file(bt)

    def test_doesnt_bundle_itself(self, challenge_ready):
        with bundle(challenge_ready) as (bt, output):
            with ZipFile(output.path, 'r') as z:
                files = z.namelist()

                assert 'bundle.zip' not in files
