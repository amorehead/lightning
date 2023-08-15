# Copyright The Lightning AI team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Warning-related utilities."""
import os
import warnings
from functools import wraps
from pathlib import Path
from typing import Callable, Optional, Type, Union

import lightning as L
from lightning.fabric.utilities.rank_zero import LightningDeprecationWarning

# enable our warnings
warnings.simplefilter("default", category=LightningDeprecationWarning)


def _wrap_formatwarning(default_format_warning: Callable) -> Callable:
    @wraps(default_format_warning)
    def wrapper(
        message: Union[Warning, str], category: Type[Warning], filename: str, lineno: int, line: Optional[str] = None
    ) -> str:
        print(L.__file__, filename)  # FIXME: debug ci

        common_path = os.path.commonpath([Path(filename).absolute(), Path(L.__file__).parent.absolute()])
        if os.path.basename(common_path) == "lightning":
            # The warning originates from the Lightning package
            return f"{filename}:{lineno}: {message}\n"
        return default_format_warning(message, category, filename, lineno, line)

    return wrapper


warnings.formatwarning = _wrap_formatwarning(warnings.formatwarning)


class PossibleUserWarning(UserWarning):
    """Warnings that could be false positives."""
