from pygdmod.rwmmem import *
from pymem.exception import ProcessNotFound

# Exceptions
class GameNotRunning(Exception):
    pass

# Number to resolution
number_to_resolution = {
    1: (640, 480),
    2: (720, 480),
    3: (720, 576),
    4: (800, 600),
    5: (1024, 768),
    6: (1152, 864),
    7: (1176, 644),
    8: (1280, 720),
    9: (1280, 768),
    10: (1280, 800),
    11: (1280, 960),
    12: (1280, 1024),
    13: (1360, 768),
    14: (1366, 768),
    15: (1440, 900),
    16: (1600, 900),
    17: (1600, 1024),
    18: (1680, 1050),
    19: (1768, 992),
    20: (1920, 1080),
}

class GeometryDashModloader:
    def __init__(self):
        try:
            game = Get_Process('GeometryDash.exe')
        except ProcessNotFound:
            raise GameNotRunning('Could not find process: GeometryDash.exe')
        self.base_address = game[1]
        self.pid = game[0]
    
    # MEMORY READS
    def getBaseAddress(self) -> int:
        return self.base_address
    def getProcessId(self) -> int:
        return self.pid
    def getScene(self) -> int:
        sceneInt = Find_Pointer(self.base_address, 0x3222D0, [0x1DC])
        return Read_Int(sceneInt)
    def getGameResolutionInt(self) -> int:
        resolutionInt = Find_Pointer(self.base_address, 0x3222D0, [0x2E0])
        return resolutionInt
    def getGameResolution(self):
        resolutionInt = Find_Pointer(self.base_address, 0x3222D0, [0x2E0])
        return number_to_resolution.get(resolutionInt, (0, 0))
    def getUsername(self) -> str:
        userName = Find_Pointer(self.base_address, 0x3222D8, [0x108])
        return Read_String(userName)
    def isDead(self) -> bool:
        try:
            isDeadPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x39C])
            return Read_Bool(isDeadPtr)
        except:
            return False
    def getLevelLength(self) -> float:
        levelLenPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x3B4])
        return Read_Float(levelLenPtr)
    def getObjectCount(self) -> int:
        objCountPtr = Find_Pointer(self.base_address, 0x3222D0, [0x168, 0x3A0])
        return Read_Int(objCountPtr)

    def getXpos(self, player = 1) -> float: # takes 1, 2, 'both'. with both it return a tuple of xpos
        if player == 1:# for p1
            xposPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x67C])
            return Read_Float(xposPtr)
        elif player == 2: # for p2
            xposPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x228, 0x67C])
            return Read_Float(xposPtr)
        elif player == 'both':
            xposPtrP1 = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x67C])
            xposPtrP2 = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x228, 0x67C])
            return (Read_Float(xposPtrP1), Read_Float(xposPtrP2))
    def getLevelPercentage(self, *, final: float = 100.0) -> float:
        try:
            percent = self.getXpos() / self.getLevelLength() * final
        except Exception:
            percent = 0.0
        return percent if percent < final else final

    # i did not discover p2 pointers yet
    def getYpos(self) -> float:
        yposPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x38])
        return Read_Float(yposPtr)

    def getPlayerSpeed(self) -> float:
        speedPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x648])
        return Read_Float(speedPtr)

    def getPlayerHitboxSize(self) -> float:
        hitboxSizePtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x644])
        return Read_Float(hitboxSizePtr)

    def isInPracticeMode(self) -> bool:
        try:
            practiceModePtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x495])
            return Read_Bool(practiceModePtr)
        except:
            return False
    
    def isInEditor(self) -> bool:
        try:
            editorPtr = Find_Pointer(self.base_address, 0x3222D0, [0x168])
            return Read_Bool(editorPtr)
        except:
            return False

    def getGravity(self) -> float:
        gravityPtr = Find_Pointer(self.base_address, 0x1E9050, [0])
        return Read_Float(gravityPtr)

    def getLevelId(self) -> int:
        levelIdPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0xF8])
        return Read_Int(levelIdPtr)

    def getLevelName(self) -> str:
        try:
            levelNamePtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0xFC])
            return Read_String(levelNamePtr)
        except:
            try:
                levelNamePtr = Find_Pointer(self.base_address, 0x3222D0, [0x168, 0x124, 0xEC, 0x110, 0x114, 0xFC])
                return Read_String(levelNamePtr)
            except:
                return None
    
    def getLevelCreatorName(self) -> str:
        try:
            levelCreatorNamePtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0x144])
            return Read_String(levelCreatorNamePtr)
        except:
            return None
    
    def getLevelStars(self) -> int:
        try:
            levelStarsPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0x2AC])
            return Read_Int(levelStarsPtr)
        except:
            return 0
    
    def getFeaturedLevelScore(self) -> int:
        try:
            levelScorePtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0x27C])
            return Read_Int(levelScorePtr)
        except:
            return 0

    def isLevelFeatured(self) -> bool:
        return self.getFeaturedLevelScore() > 0

    def isLevelEpic(self) -> bool:
        try:
            levelEpicPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0x280])
            return Read_Bool(levelEpicPtr)
        except:
            return False
    
    def isLevelDemon(self) -> bool:
        try:
            levelDemonPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0x29C])
            return Read_Bool(levelDemonPtr)
        except:
            return False

    def isLevelAuto(self) -> bool:
        try:
            levelAutoPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0x2B0])
            return Read_Bool(levelAutoPtr)
        except:
            return False
        
    def getDemonDifficulity(self) -> int:
        try:
            demonDiffPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0x2A0])
            return Read_Int(demonDiffPtr)
        except:
            return 0
    
    def getTotalJumps(self) -> int:
        try:
            totalJumpsPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114, 0x224])
            return Read_Int(totalJumpsPtr)
        except:
            return 0

    def isInLevel(self) -> bool:
        try:
            isInLevelPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x22C, 0x114])
            return Read_Bool(isInLevelPtr)
        except:
            return False

    def getSongId(self) -> int:
        try:
            songIdPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x488, 0x1C4])
            return Read_Int(songIdPtr)
        except:
            return False
    
    def getAttempt(self) -> int:
        try:
            attemptPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x4A8])
            return Read_Int(attemptPtr)
        except:
            return False

    def getSpeedhack(self) -> float:
        try:
            speedhackPtr = Find_Pointer(self.base_address, 0x3222D0, [0xCC, 0x20])
            return Read_Float(speedhackPtr)
        except:
            return 0
    
    def isInEndscreen(self) -> bool:
        try:
            endscreenPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x4E0])
            return Read_Bool(endscreenPtr)
        except:
            return False

    # MEMORY WRITES
    # accept player: 1; 2; 'both'
    def setXpos(self, pos: float, player = 1) -> None:
        if player == 1:
            xposPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x67C])
            Write_Mem(xposPtr, New_Value=pos, float_or_int=1)
        elif player == 2: # change for p2
            xposPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x228, 0x67C])
            Write_Mem(xposPtr, New_Value=pos, float_or_int=1)
        elif player == 'both':
            xposPtrP1 = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x67C])
            xposPtrP2 = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x228, 0x67C])
            Write_Mem(xposPtrP1, New_Value=pos, float_or_int=1)
            Write_Mem(xposPtrP2, New_Value=pos, float_or_int=1)
        else:
            xposPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x67C])
            Write_Mem(xposPtr, New_Value=pos, float_or_int=1)

    # i did not discover p2 pointers yet
    def setYpos(self, pos: float) -> None:
        yposPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x38])
        Write_Mem(yposPtr, New_Value=pos, float_or_int=1)

    def setPlayerSpeed(self, speedValue: float) -> None:
        speedPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x648])
        Write_Mem(address=speedPtr, New_Value=speedValue, float_or_int=1)
    
    def setPlayerHitboxSize(self, newSize: float) -> None:
        hitboxSizePtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x35C])
        hitboxSizePtr2 = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x224, 0x644])
        Write_Mem(address=hitboxSizePtr, New_Value=newSize, float_or_int=1)
        Write_Mem(address=hitboxSizePtr2, New_Value=newSize, float_or_int=1)

    def setGravity(self, newGravity: float) -> None:
        gravityPtr = Find_Pointer(self.base_address, 0x1E9050, [0])
        Write_Mem(address=gravityPtr, New_Value=newGravity, float_or_int=1)
    
    def setAttempt(self, attempt: int) -> None:
        attemptPtr = Find_Pointer(self.base_address, 0x3222D0, [0x164, 0x4A8])
        Write_Mem(address=attemptPtr, New_Value=attempt, float_or_int=0)
