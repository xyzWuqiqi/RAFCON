# Copyright (C) 2015-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the Eclipse Public License v1.0 which
# accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
# Annika Wollschlaeger <annika.wollschlaeger@dlr.de>
# Franz Steinmetz <franz.steinmetz@dlr.de>
# Lukas Becker <lukas.becker@dlr.de>
# Mahmoud Akl <mahmoud.akl@dlr.de>
# Matthias Buettner <matthias.buettner@dlr.de>
# Michael Vilzmann <michael.vilzmann@dlr.de>
# Rico Belder <rico.belder@dlr.de>
# Sebastian Brunner <sebastian.brunner@dlr.de>

"""
.. module:: state_editor
   :synopsis: A module that holds the state editor controller which provides footage all sub-state-element-controllers.

"""

from rafcon.core.states.library_state import LibraryState

from rafcon.gui.controllers.state_editor.data_flows import StateDataFlowsEditorController
from rafcon.gui.controllers.state_editor.description_editor import DescriptionEditorController
from rafcon.gui.controllers.state_editor.io_data_port_list import InputPortListController, OutputPortListController
from rafcon.gui.controllers.state_editor.linkage_overview import LinkageOverviewController
from rafcon.gui.controllers.state_editor.outcomes import StateOutcomesEditorController
from rafcon.gui.controllers.state_editor.overview import StateOverviewController
from rafcon.gui.controllers.state_editor.scoped_variable_list import ScopedVariableListController
from rafcon.gui.controllers.state_editor.source_editor import SourceEditorController
from rafcon.gui.controllers.state_editor.transitions import StateTransitionsEditorController
from rafcon.gui.controllers.utils.extended_controller import ExtendedController
from rafcon.gui.controllers.state_editor.semantic_data_editor import SemanticDataEditorController
from rafcon.gui.models import ContainerStateModel, AbstractStateModel, LibraryStateModel
from rafcon.gui.views.state_editor.state_editor import StateEditorView

from rafcon.utils import log
logger = log.get_logger(__name__)


class StateEditorController(ExtendedController):
    """Controller handles the organization of the Logic-Data oriented State-Editor.
    Widgets concerning logic flow (outcomes and transitions) are grouped in the Logic Linkage expander.
    Widgets concerning data flow (data-ports and data-flows) are grouped in the data linkage expander.

    :param rafcon.gui.models.state.StateModel model: The state model
    """

    def __init__(self, model, view):
        """Constructor"""
        assert isinstance(model, AbstractStateModel)
        assert isinstance(view, StateEditorView)
        ExtendedController.__init__(self, model, view)

        sv_and_source_script_state_m = model.state_copy if isinstance(model, LibraryStateModel) else model

        self.add_controller('properties_ctrl', StateOverviewController(model, view.properties_view))

        self.inputs_ctrl = InputPortListController(model, view.inputs_view)
        self.add_controller('input_data_ports', self.inputs_ctrl)
        self.outputs_ctrl = OutputPortListController(model, view.outputs_view)
        self.add_controller('output_data_ports', self.outputs_ctrl)
        self.scopes_ctrl = ScopedVariableListController(sv_and_source_script_state_m, view.scopes_view)
        self.add_controller('scoped_variables', self.scopes_ctrl)
        self.add_controller('outcomes', StateOutcomesEditorController(model, view.outcomes_view))

        self.add_controller('transitions_ctrl', StateTransitionsEditorController(model, view.transitions_view))
        self.add_controller('data_flows_ctrl', StateDataFlowsEditorController(model, view.data_flows_view))

        self.add_controller('linkage_overview_ctrl', LinkageOverviewController(model, view.linkage_overview))

        self.add_controller('description_ctrl', DescriptionEditorController(model, view.description_view))
        if not isinstance(model, ContainerStateModel) and not isinstance(model, LibraryStateModel) or \
                isinstance(model, LibraryStateModel) and not isinstance(model.state_copy, ContainerStateModel):
            self.add_controller('source_ctrl', SourceEditorController(sv_and_source_script_state_m, view.source_view))
        self.add_controller('semantic_data_ctrl', SemanticDataEditorController(model, view.semantic_data_view))

    def register_view(self, view):
        """Called when the View was registered

        Can be used e.g. to connect signals. Here, the destroy signal is connected to close the application
        """
        view['add_input_port_button'].connect('clicked', self.inputs_ctrl.on_add)
        view['add_output_port_button'].connect('clicked', self.outputs_ctrl.on_add)
        view['add_scoped_variable_button'].connect('clicked', self.scopes_ctrl.on_add)

        view['remove_input_port_button'].connect('clicked', self.inputs_ctrl.on_remove)
        view['remove_output_port_button'].connect('clicked', self.outputs_ctrl.on_remove)
        view['remove_scoped_variable_button'].connect('clicked', self.scopes_ctrl.on_remove)

        if isinstance(self.model, LibraryStateModel) or self.model.state.get_library_root_state():
            view['add_input_port_button'].set_sensitive(False)
            view['remove_input_port_button'].set_sensitive(False)
            view['add_output_port_button'].set_sensitive(False)
            view['remove_output_port_button'].set_sensitive(False)
            view['add_scoped_variable_button'].set_sensitive(False)
            view['remove_scoped_variable_button'].set_sensitive(False)

        view.inputs_view.show()
        view.outputs_view.show()
        view.scopes_view.show()
        view.outcomes_view.show()
        view.transitions_view.show()
        view.data_flows_view.show()

        # show scoped variables if show content is enabled -> if disabled the tab stays and indicates a container state
        if isinstance(self.model, LibraryStateModel) and not self.model.show_content():
            view.scopes_view.hide()
            view.linkage_overview.scope_view.hide()

        # Container states do not have a source editor and library states does not show there source code
        # Thus, for those states we do not have to add the source controller and can hide the source code tab
        # logger.info("init state: {0}".format(model))
        lib_with_and_ES_as_root = isinstance(self.model, LibraryStateModel) and \
                                  not isinstance(self.model.state_copy, ContainerStateModel)
        if not isinstance(self.model, ContainerStateModel) and not isinstance(self.model, LibraryStateModel) or \
                lib_with_and_ES_as_root:
            view.source_view.show()
            if isinstance(self.model, LibraryStateModel) and not self.model.show_content():
                view.remove_source_tab()
            view.remove_scoped_variables_tab()
        else:
            view.scopes_view.show()
            if isinstance(self.model, LibraryStateModel) and \
                    (not self.model.show_content() or not isinstance(self.model.state_copy, ContainerStateModel)):
                view.remove_scoped_variables_tab()
            view.remove_source_tab()

        if isinstance(self.model.state, LibraryState):
            view.bring_tab_to_the_top('Description')
        else:
            view.bring_tab_to_the_top('Linkage Overview')

        if isinstance(self.model, ContainerStateModel):
            self.scopes_ctrl.reload_scoped_variables_list_store()

    def register_adapters(self):
        """Adapters should be registered in this method call

        Each property of the state should have its own adapter, connecting a label in the View with the attribute of
        the State.
        """
        # self.adapt(self.__state_property_adapter("name", "input_name"))

    def rename(self):
        state_overview_controller = self.get_controller('properties_ctrl')
        state_overview_controller.rename()

    @ExtendedController.observe("meta_signal", signal=True)
    def show_content_changed(self, model, prop_name, info):
        meta_signal_message = info['arg']
        if meta_signal_message.change == 'show_content':
            if self.model.meta['gui']['show_content']:
                if isinstance(model.state_copy, ContainerStateModel):
                    self.view.insert_scoped_variables_tab()
                else:
                    self.view.insert_source_tab()
                self.view.linkage_overview.scope_view.show()
            else:
                if isinstance(model.state_copy, ContainerStateModel):
                    self.view.remove_scoped_variables_tab()
                else:
                    self.view.remove_source_tab()
                self.view.linkage_overview.scope_view.hide()

    @ExtendedController.observe("action_signal", signal=True)
    def state_type_changed(self, model, prop_name, info):
        """Reopen state editor when state type is changed

        When the type of the observed state changes, a new model is created. The look of this controller's view
        depends on the kind of model. Therefore, we have to destroy this editor and open a new one with the new model.
        """
        msg = info['arg']
        # print self.__class__.__name__, "state_type_changed check", info
        if msg.action in ['change_state_type', 'change_root_state_type'] and msg.after:
            # print self.__class__.__name__, "state_type_changed"
            import rafcon.gui.singleton as gui_singletons
            msg = info['arg']
            new_state_m = msg.affected_models[-1]
            states_editor_ctrl = gui_singletons.main_window_controller.get_controller('states_editor_ctrl')
            states_editor_ctrl.recreate_state_editor(self.model, new_state_m)
