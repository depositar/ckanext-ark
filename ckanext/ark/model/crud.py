from ckan.model import Session

from ckanext.ark.model.ark import ARK, ark_table


class ARKQuery:
    '''Query methods for ARK table.
    '''
    m = ARK
    cols = [c.name for c in ark_table.c]

    @classmethod
    def create(cls, identifier, package_id, who='', what='', when=''):
        '''Create a new record in the ARK table.

        :param identifier: the compact ARK without the 'ark:' part
        :type identifier: string
        :param package_id: the id of the package this ARK represents
        :type package_id: string

        :returns: the newly created record object
        '''
        new_record = ARK(identifier=identifier,
                         package_id=package_id,
                         who=who,
                         what=what,
                         when=when)
        Session.add(new_record)
        Session.commit()
        return new_record

    @classmethod
    def read_ark(cls, identifier):
        '''Retrieve a record with a given ARK.

        :param identifier: the compact ARK without the 'ark:' part
        :type identifier: string

        :returns: the record object
        '''
        return Session.query(ARK).get(identifier)

    @classmethod
    def read_package(cls, package_id, create_if_none=False):
        '''Retrieve a record associated with a given package.

        :param package_id: the id of the package
        :type package_id: string
        :param create_if_none: generate a new ARK and add a record if no record
                               is found for the given package
                               (optional, default: False)
        :type create_if_none: bool

        :returns: the record object
        '''
        from ckanext.ark.lib.minter import Minter
        record = (Session.query(ARK).filter(ARK.package_id == package_id)
                  .first())
        if record is None and create_if_none:
            minter = Minter()
            new_ark = minter.mint_ark()
            record = cls.create(identifier=new_ark, package_id=package_id)
        return record

    @classmethod
    def update_ark(cls, identifier, **kwargs):
        '''Update the published fields of a record with a given ARK.

        :param identifier: the compact ARK without the 'ark:' part
        :type identifier: string
        :param kwargs: the values to be updated
        :type kwargs: dictionary

        :returns: the updated record object
        '''
        update_dict = {k: v for k, v in kwargs.items() if k in cls.cols}
        (Session.query(ARK).filter(ARK.identifier == identifier)
         .update(update_dict))
        Session.commit()
        return cls.read_ark(identifier)

    @classmethod
    def delete_ark(cls, identifier):
        '''Delete the record with a given ARK.

        :param identifier: the compact ARK without the 'ark:' part
        :type identifier: string

        :returns: True if a record was deleted, False if not
        :rtype: bool
        '''
        to_delete = cls.read_ark(identifier)
        if to_delete is not None:
            Session.delete(to_delete)
            Session.commit()
            return True
        else:
            return False
