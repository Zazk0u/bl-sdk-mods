import unrealsdk
from Mods.ModMenu import ModTypes, EnabledSaveType, RegisterMod, SDKMod, Hook 

class OpenSesame(SDKMod):
	Name: str = "Open Sesame"
	Author: str = "Zazk0u"
	Description: str = "Allow you to damage chests and containers to open them."
	Version: str = "1.0.0"
	Types: ModTypes = ModTypes.Gameplay
	SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadOnMainMenu
	
	INTERACTIVE_OBJECT_CLASS: unrealsdk.UClass = unrealsdk.FindClass("WillowInteractiveObject")
	ALLEGIANCE: unrealsdk.UObject = unrealsdk.FindObject("PawnAllegiance", "GD_AI_Allegiance.Allegiance_Player")

	@Hook("WillowGame.WillowInteractiveObject.InitializeFromDefinition")
	def on_initialize(
		self, this: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct
	)-> bool:
		#Check if the object's class name is correct and has loot.
		if not this.Loot or this.Class is not self.INTERACTIVE_OBJECT_CLASS: 
			return True
		#Set allegiance to player which prevent damaged enemy events to work. bCanTakeDirectDamage check for vanilla objects that could receive damage and exclude them, cause Anarchy prestackers would kill me.
		if not params.Definition.Allegiance and not params.Definition.bCanTakeDirectDamage: 
			params.Definition.Allegiance = self.ALLEGIANCE
			
		params.Definition.bCanTakeDirectDamage = True  
		params.Definition.bCanTakeRadiusDamage = True
		return True
	
	@Hook("WillowGame.WillowInteractiveObject.TakeDamage")
	def on_take_damage(
		self, this: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct
	)-> bool:
		#Check if the damage was dealt by a player.
		if not params.EventInstigator.Pawn.IsHumanControlled(): 
			return True
		#Check if the object's class name is correct and has loot.
		if not this.Loot or this.Class is not self.INTERACTIVE_OBJECT_CLASS: 
			return True
		#Check if the object cost nothing and can be used.
		if this.bCostsToUse[0] != 0 or this.bCanBeUsed[0] != 1: 
			return True

		this.UseObject(params.EventInstigator.Pawn, None, 0)
		return True

	def Enable(self) -> None:
		super().Enable()

	def Disable(self) -> None:
		super().Disable()

...
RegisterMod(OpenSesame())

