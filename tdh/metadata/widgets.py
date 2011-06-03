import zope.component
import zope.interface
import zope.location
from z3c.form import action, button, interfaces
from z3c.form.widget import FieldWidget
from z3c.form.browser.button import ButtonWidget

from plone.formwidget.autocomplete.widget import \
        AutocompleteMultiSelectionWidget

from collective.z3cform.datagridfield import DataGridField

class AnzrscCodeDataGridField(DataGridField):
    code_type = ''
    code_levels = 3

class ForCodeDataGridField(AnzrscCodeDataGridField):
    code_type = 'for'

class SeoCodeDataGridField(AnzrscCodeDataGridField):
    code_type = 'seo'

@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def ForCodeDataGridFieldFactory(field, request):
    """IFieldWidget factory for DataGridField."""
    return FieldWidget(field, ForCodeDataGridField(request))

@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def SeoCodeDataGridFieldFactory(field, request):
    """IFieldWidget factory for DataGridField."""
    return FieldWidget(field, SeoCodeDataGridField(request))


class StandardButtonAction(action.Action, ButtonWidget, zope.location.Location):
    """Button action class for standard buttons (not submit!)"""
    zope.interface.implements(interfaces.IButtonAction)
    zope.component.adapts(interfaces.IFormLayer, interfaces.IButton)

    def __init__(self, request, field):
        action.Action.__init__(self, request, field.title)
        ButtonWidget.__init__(self, request)
        self.field = field

    accesskey = button.ButtonAction.accesskey
    value = button.ButtonAction.value
    id = button.ButtonAction.id

def standardButtonActionFactory(request, field):
    """Factory for producing standard button actions"""
    button = StandardButtonAction(request, field)
    import ipdb; ipdb.set_trace()
    return button


class UnrestrictedAutocompleteSelectionWidget(AutocompleteMultiSelectionWidget):
    mustMatch = False
    newTermButton = u"Add new"

    extra_js = """

    (function($) {

        $().ready(function() {
            $('#%(id)s-buttons-add').unbind('click').click(function() {
                field = $('#%(id)s-widgets-query');
                value = field.val();
                if (value) {
                    formwidget_autocomplete_new_value(field, value, value);
                }
                return false;
            });
        });

    })(jQuery);

    """


    def render(self):
        add_term_button = button.Button("add", title=self.newTermButton)
        add_term_button.actionFactory = standardButtonActionFactory
        self.subform.buttons += button.Buttons(add_term_button)
        self.subform.update()

        position = self.js_template.find("/* ]]> */")
        self.js_template = self.js_template[:position] + self.extra_js + \
                self.js_template[position:]

        return super(UnrestrictedAutocompleteSelectionWidget, self).render()

@zope.interface.implementer(interfaces.IFieldWidget)
def UnrestrictedAutocompleteMultiFieldWidget(field, request):
    """IFieldWidget factory for custom AutocompleteMultiFieldWidget."""
    return FieldWidget(field, \
                       UnrestrictedAutocompleteSelectionWidget(request))

