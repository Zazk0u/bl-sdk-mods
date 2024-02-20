import unrealsdk
from Mods.ModMenu import ModTypes, EnabledSaveType, RegisterMod, SDKMod, Hook 

class OpenSesame(SDKMod):
	Name: str = "Open Sesame"
	Author: str = "Zazk0u"
	Description: str = "Allow you to damage chests and containers to open them."
	Version: str = "1.1.0"
	Types: ModTypes = ModTypes.Gameplay
	SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadOnMainMenu
	
	BASE_INTERACTIVE_OBJECT_CLASS: unrealsdk.UClass = unrealsdk.FindClass("WillowInteractiveObject")
	ALLEGIANCE: unrealsdk.UObject 					= unrealsdk.FindObject("PawnAllegiance", "GD_AI_Allegiance.Allegiance_FullNeutral")

	def has_loot_and_base_class(self, WIO)-> bool:
		return WIO.Loot and WIO.Class is self.BASE_INTERACTIVE_OBJECT_CLASS
		
	@Hook("WillowGame.WillowInteractiveObject.InitializeFromDefinition")
	def on_initialize(self, WIO: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct)-> bool:
		IO_definition = WIO.Definition

		if not IO_definition or not self.has_loot_and_base_class(WIO): 
			return True
		
		# Prevent on damage enemies checks by settings the allegiance to neutral.
		# bCanTakeDirectDamage check for any vanilla objects that could already receive damage and exclude them, specifically so Anarchy prestackers can still stack from some containers.
		if not IO_definition.Allegiance and not IO_definition.bCanTakeDirectDamage: 
			IO_definition.Allegiance = self.ALLEGIANCE
		
		# This allow the WillowInteractiveObject TakeDamage method to be called.
		IO_definition.bCanTakeDirectDamage = True  
		IO_definition.bCanTakeRadiusDamage = True
		return True
	
	@Hook("WillowGame.WillowInteractiveObject.TakeDamage")
	def on_take_damage(self, WIO: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct)-> bool:
		controller = params.EventInstigator

		if not controller or not controller.bIsHumanPlayer or not self.has_loot_and_base_class(WIO): 
			return True

		if not WIO.bCostsToUse[0] == 0 or not WIO.bCanBeUsed[0] == 1: 
			return True

		WIO.UseObject(controller.Pawn, None, 0)
		return True

	def Enable(self) -> None:
		super().Enable()

	def Disable(self) -> None:
		super().Disable()

...
RegisterMod(OpenSesame())
