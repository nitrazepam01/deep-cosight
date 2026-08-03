# Co-Sight Integration

The adapter targets Co-Sight commit
`28150a4c02c438418fdeaefbefd4654727e209ae`.

## Install And Check

1. Install this package into the same Python environment as Co-Sight:

   ```powershell
   python -m pip install G:\path\to\CoSightControlSkill
   ```

2. From the Co-Sight repository root, verify and apply the patch:

   ```powershell
   git apply --check G:\path\to\CoSightControlSkill\integration\cosight\register_control_skill.patch
   git apply G:\path\to\CoSightControlSkill\integration\cosight\register_control_skill.patch
   ```

3. Add the six names in `agents.fragment.json` to the intended actor. The supplied
   patch adds them to `builtin-actor`.

4. Merge `CONTROL_FUNCTION_ARG_MAPPING` into `FUNCTION_ARG_MAPPING` if alias
   normalization is wanted. The public JSON names work without aliases.

5. Run the adapter smoke test from this package, then start Co-Sight normally.

The patch adds only two adapter files and small registry mappings. It does not
copy the numerical core into Co-Sight and does not alter `execute_code`.

