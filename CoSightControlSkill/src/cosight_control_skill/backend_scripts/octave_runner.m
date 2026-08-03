function octave_runner(request_path, response_path)
  pkg load control;
  request = jsondecode(fileread(request_path));
  plant = request.plant;
  if strcmp(plant.representation, "transfer_function")
    if strcmp(plant.timebase.kind, "discrete")
      system = tf(plant.numerator(:).', plant.denominator(:).', plant.timebase.dt);
    else
      system = tf(plant.numerator(:).', plant.denominator(:).');
    endif
    if isfield(request.controller, "representation") && strcmp(request.controller.representation, "transfer_function")
      model = request.controller.model;
      if isfield(model, "dt") && !isempty(model.dt)
        controller = tf(model.numerator(:).', model.denominator(:).', model.dt);
      else
        controller = tf(model.numerator(:).', model.denominator(:).');
      endif
    else
      controller = tf(1, 1);
    endif
    loop = minreal(controller * system);
    if strcmp(request.configuration, "open_loop")
      response_system = loop;
    else
      feedback_sign = -1;
      if strcmp(request.feedback.sign, "positive")
        feedback_sign = 1;
      endif
      response_system = feedback(loop, request.feedback.gain, feedback_sign);
    endif
  else
    if strcmp(plant.timebase.kind, "discrete")
      system = ss(plant.A, plant.B, plant.C, plant.D, plant.timebase.dt);
    else
      system = ss(plant.A, plant.B, plant.C, plant.D);
    endif
    response_system = system;
    if strcmp(request.configuration, "closed_loop") && isfield(request.controller, "representation") && strcmp(request.controller.representation, "state_feedback")
      K = request.controller.gain_matrix;
      reference_gain = 1;
      if isfield(request.controller, "reference_gain")
        reference_gain = request.controller.reference_gain;
      endif
      response_system = ss(system.a - system.b * K, system.b * reference_gain, system.c, system.d * reference_gain, system.tsam);
    endif
  endif
  requested_time = request.time(:);
  [step_values, step_time] = step(response_system, requested_time);
  poles = pole(response_system);
  result = struct();
  result.backend = "octave";
  result.available = true;
  result.step_time = step_time(:).';
  result.step_values = squeeze(step_values).';
  result.poles_real = real(poles(:)).';
  result.poles_imag = imag(poles(:)).';
  handle = fopen(response_path, "w");
  if handle < 0
    error("Unable to open response path");
  endif
  fwrite(handle, jsonencode(result), "char");
  fclose(handle);
endfunction
