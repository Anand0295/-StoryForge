import termcolor
import datetime
import os
import json

def PrintMessageHistory(_Messages):
    print("------------------------------------------------------------")
    for Message in _Messages:
        print(Message)
    print("------------------------------------------------------------")

class Logger:
    def __init__(self, _LogfilePrefix="Logs"):
        try:
            # Validate and sanitize input to prevent path traversal (CWE-22)
            _LogfilePrefix = self._sanitize_path(_LogfilePrefix)
            
            # Make Paths For Log
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            LogDirPath = os.path.join(_LogfilePrefix, f"Generation_{timestamp}")
            
            # Resolve to absolute path and verify it's within the expected directory
            LogDirPath = os.path.abspath(LogDirPath)
            base_path = os.path.abspath(_LogfilePrefix)
            
            if not LogDirPath.startswith(base_path):
                raise ValueError(f"Path traversal detected: {LogDirPath}")
            
            # Create directories with error handling
            langchain_debug_path = os.path.join(LogDirPath, "LangchainDebug")
            os.makedirs(langchain_debug_path, exist_ok=True)
            
            # Setup Log Path
            self.LogDirPrefix = LogDirPath
            self.LogPath = os.path.join(LogDirPath, "Main.log")
            self.File = open(self.LogPath, "a", encoding='utf-8')
            self.LangchainID = 0
            self.LogItems = []
        except (OSError, IOError, ValueError) as e:
            print(f"Error initializing Logger: {e}")
            raise
    
    def _sanitize_path(self, path):
        """Sanitize path to prevent traversal attacks"""
        if not path:
            raise ValueError("Path cannot be empty")
        
        # Remove any null bytes
        path = path.replace('\0', '')
        
        # Normalize path and remove dangerous patterns
        path = os.path.normpath(path)
        
        # Check for path traversal attempts
        if '..' in path or path.startswith('/') or path.startswith('\\'):
            raise ValueError(f"Invalid path: {path}")
        
        return path
    
    def _validate_filename(self, filename):
        """Validate filename to prevent directory traversal"""
        if not filename:
            raise ValueError("Filename cannot be empty")
        
        # Remove null bytes and dangerous characters
        filename = filename.replace('\0', '').replace('/', '').replace('\\', '')
        
        # Check for path traversal patterns
        if '..' in filename:
            raise ValueError(f"Invalid filename: {filename}")
        
        return filename
    
    def _secure_path_join(self, base_path, *paths):
        """Securely join paths and verify result is within base path"""
        joined_path = os.path.join(base_path, *paths)
        joined_path = os.path.abspath(joined_path)
        base_path = os.path.abspath(base_path)
        
        if not joined_path.startswith(base_path):
            raise ValueError(f"Path traversal detected: {joined_path}")
        
        return joined_path

    # Helper function that saves the entire language chain object as both json and markdown for debugging later
    def SaveLangchain(self, _LangChainID:str, _LangChain:list):
        try:
            # Validate input
            if not _LangChainID:
                raise ValueError("LangChainID cannot be empty")
            if not isinstance(_LangChain, list):
                raise TypeError("LangChain must be a list")
            
            # Sanitize the LangChainID to prevent path traversal
            sanitized_id = self._validate_filename(str(_LangChainID))
            
            # Calculate Filepath For This Langchain
            filename_base = f"{self.LangchainID}_{sanitized_id}"
            ThisLogPathJSON = self._secure_path_join(self.LogDirPrefix, "LangchainDebug", f"{filename_base}.json")
            ThisLogPathMD = self._secure_path_join(self.LogDirPrefix, "LangchainDebug", f"{filename_base}.md")
            LangChainDebugTitle = filename_base
            self.LangchainID += 1
            
            # Generate and Save JSON Version
            with open(ThisLogPathJSON, "w", encoding='utf-8') as f:
                f.write(json.dumps(_LangChain, indent=4, sort_keys=True))
            
            # Now, Save Markdown Version
            with open(ThisLogPathMD, "w", encoding='utf-8') as f:
                MarkdownVersion = f"# Debug LangChain {LangChainDebugTitle}\n**Note: '```' tags have been removed in this version.**\n"
                for Message in _LangChain:
                    if not isinstance(Message, dict):
                        continue
                    role = Message.get('role', 'unknown')
                    content = Message.get('content', '')
                    MarkdownVersion += f"\n\n\n# Role: {role}\n"
                    MarkdownVersion += f"```{content.replace('```', '')}```"
                f.write(MarkdownVersion)
            
            self.Log(f"Wrote This Language Chain ({LangChainDebugTitle}) To Debug File {ThisLogPathMD}", 5)
        except (OSError, IOError, ValueError, TypeError) as e:
            error_msg = f"Error saving langchain: {e}"
            print(error_msg)
            self.Log(error_msg, 7)
    
    # Saves the given story to disk
    def SaveStory(self, _StoryContent:str):
        try:
            # Validate input
            if not isinstance(_StoryContent, str):
                raise TypeError("Story content must be a string")
            
            # Securely construct path
            story_path = self._secure_path_join(self.LogDirPrefix, "Story.md")
            
            with open(story_path, "w", encoding='utf-8') as f:
                f.write(_StoryContent)
            
            self.Log(f"Wrote Story To Disk At {story_path}", 5)
        except (OSError, IOError, TypeError, ValueError) as e:
            error_msg = f"Error saving story: {e}"
            print(error_msg)
            self.Log(error_msg, 7)
    
    # Logs an item
    def Log(self, _Item, _Level:int):
        try:
            # Validate input
            if not isinstance(_Level, int):
                _Level = 0
            
            # Create Log Entry
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            LogEntry = f"[{str(_Level).ljust(2)}] [{timestamp}] {_Item}"
            
            # Write it to file
            if hasattr(self, 'File') and self.File and not self.File.closed:
                self.File.write(LogEntry + "\n")
                self.File.flush()  # Ensure write is completed
            
            self.LogItems.append(LogEntry)
            
            # Now color and print it
            color_map = {
                0: "white",
                1: "grey",
                2: "blue",
                3: "cyan",
                4: "magenta",
                5: "green",
                6: "yellow",
                7: "red"
            }
            
            color = color_map.get(_Level, "white")
            LogEntry = termcolor.colored(LogEntry, color)
            print(LogEntry)
        except (OSError, IOError) as e:
            print(f"Error logging: {e}")
    
    def __del__(self):
        try:
            if hasattr(self, 'File') and self.File and not self.File.closed:
                self.File.close()
        except Exception as e:
            print(f"Error closing log file: {e}")
