Verifying adr repo directory 'docs\adr' exists... 

  PyadrAdrDirectoryDoesNotExistsError

  

  at ~\AppData\Roaming\Python\Python314\site-packages\pyadr\core.py:534 in verify_adr_dir_exists
      530│             logger.error(
      531│                 f"Directory '{adr_repo_path}/' does not exist. "
      532│                 "Initialise your ADR repo first."
      533│             )
    → 534│             raise PyadrAdrDirectoryDoesNotExistsError()
      535│         logger.log("VERBOSE", "... done.")
      536│ 
