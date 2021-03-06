from ckan.common import OrderedDict, _
from ckan.plugins import toolkit
from ckanext.googleanalytics.model import PackageStats, ResourceStats


def google_analytics_dataset_report(last):
    '''
    Generates report based on google analytics data. number of views per package
    '''
    # get package objects corresponding to popular GA content
    result = PackageStats.get_top(limit=last)
    packages = []

    for package in result['packages']:
        package_with_extras = toolkit.get_action('package_show')({}, {'id': package['package_id']})
        package_with_extras['visits'] = package['visits']
        package_with_extras['visit_date'] = package['visit_date']
        packages.append(package_with_extras)

    from operator import itemgetter
    result['packages'] = sorted(packages, key=itemgetter('visits'), reverse=True)

    return {
        'table': result.get("packages")
    }

def google_analytics_dataset_option_combinations():
    options = [20,25,30,35,40,45,50]
    for option in options:
        yield { 'last': option }

googleanalytics_dataset_report_info = {
    'name': 'google-analytics-dataset',
    'title': 'Most popular datasets',
    'description': 'Google analytics showing top datasets with most views',
    'option_defaults': OrderedDict((('last',20),)),
    'option_combinations': google_analytics_dataset_option_combinations,
    'generate': google_analytics_dataset_report,
    'template': 'report/dataset_analytics.html',
    }


def google_analytics_resource_report(last):
    '''
    Generates report based on google analytics data. number of views per package
    '''
    # get resource objects corresponding to popular GA content
    top_resources = ResourceStats.get_top(limit=last)

    for resource in top_resources.get("resources", []):
        resource['resource'] = toolkit.get_action('resource_show')({"ignore_auth": True}, {"id": resource.get('resource_id')})
        resource['package'] = toolkit.get_action('package_show')({"ignore_auth": True}, {"id": resource.get('package_id')})

    return {
        'table' : top_resources.get("resources")
    }

def google_analytics_resource_option_combinations():
    options = [20,25,30,35,40,45,50]
    for option in options:
        yield { 'last': option }

googleanalytics_resource_report_info = {
    'name': 'google-analytics-resource',
    'title': 'Most popular resources',
    'description': 'Google analytics showing most downloaded resources',
    'option_defaults': OrderedDict((('last',20),)),
    'option_combinations': google_analytics_resource_option_combinations,
    'generate': google_analytics_resource_report,
    'template': 'report/resource_analytics.html'
}

