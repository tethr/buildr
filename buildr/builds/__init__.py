import pkg_resources

builds = dict([(ep.name, ep.load()(ep.name)) for ep in
            pkg_resources.iter_entry_points('buildr.builds')])


